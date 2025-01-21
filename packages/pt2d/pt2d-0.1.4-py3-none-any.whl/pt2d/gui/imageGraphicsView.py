from scipy.signal import savgol_filter
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtCore import Qt, QRectF, QPoint
import math
import numpy as np
from .panZoomGraphicsView import PanZoomGraphicsView
from .labeledPointItem import LabeledPointItem
from ..find_path import find_path


class ImageGraphicsView(PanZoomGraphicsView):
    """
    A custom QGraphicsView for displaying and interacting with an image.

    This class extends PanZoomGraphicsView to provide additional functionality
    for loading images, adding labeled anchor points, and computing paths
    between points based on a cost image.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Image display
        self.image_item = QGraphicsPixmapItem()
        self.scene.addItem(self.image_item)

        self.anchor_points = []    
        self.point_items = []      
        self.full_path_points = [] 
        self._full_path_xy = []    

        self.dot_radius = 4
        self.path_radius = 1
        self.radius_cost_image = 2
        self._img_w = 0
        self._img_h = 0

        self._mouse_pressed = False
        self._press_view_pos = None
        self._drag_threshold = 5
        self._was_dragging = False
        self._dragging_idx = None
        self._drag_offset = (0, 0)
        self._drag_counter = 0

        # Cost images
        self.cost_image_original = None
        self.cost_image = None

        # Rainbow toggle => start with OFF
        self._rainbow_enabled = False

        # Smoothing parameters
        self._savgol_window_length = 22

    def set_rainbow_enabled(self, enabled: bool):
        """Enable rainbow coloring of the path."""
        self._rainbow_enabled = enabled
        self._rebuild_full_path()

    def toggle_rainbow(self):
        """Toggle rainbow coloring of the path."""
        self._rainbow_enabled = not self._rainbow_enabled
        self._rebuild_full_path()

    def set_savgol_window_length(self, wlen: int):
        """Set the window length for Savitzky-Golay smoothing."""
        wlen = max(3, wlen)
        if wlen % 2 == 0:
            wlen += 1
        self._savgol_window_length = wlen

        self._rebuild_full_path()

    # --------------------------------------------------------------------
    # LOADING
    # --------------------------------------------------------------------
    def load_image(self, path: str):
        """Load an image from a file path."""
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            self.image_item.setPixmap(pixmap)
            self.setSceneRect(QRectF(pixmap.rect()))

            self._img_w = pixmap.width()
            self._img_h = pixmap.height()

            self._clear_all_points()
            self.resetTransform()
            self.fitInView(self.image_item, Qt.KeepAspectRatio)

            # By default, add S/E
            s_x, s_y = 0.15 * self._img_w, 0.5 * self._img_h
            e_x, e_y = 0.85 * self._img_w, 0.5 * self._img_h
            self._insert_anchor_point(-1, s_x, s_y, label="S", removable=False, z_val=100, radius=6)
            self._insert_anchor_point(-1, e_x, e_y, label="E", removable=False, z_val=100, radius=6)

    # --------------------------------------------------------------------
    # ANCHOR POINTS
    # --------------------------------------------------------------------
    def _insert_anchor_point(self, idx, x: float, y: float, label="", removable=True,
                             z_val=0, radius=4):
        """Insert an anchor point at a specific index."""
        x_clamped = self._clamp(x, radius, self._img_w - radius)
        y_clamped = self._clamp(y, radius, self._img_h - radius)

        if idx < 0:
            # Insert before E if there's at least 2 anchors
            if len(self.anchor_points) >= 2:
                idx = len(self.anchor_points) - 1
            else:
                idx = len(self.anchor_points)

        self.anchor_points.insert(idx, (x_clamped, y_clamped))
        color = Qt.green if label in ("S", "E") else Qt.red
        item = LabeledPointItem(x_clamped, y_clamped,
                                label=label, radius=radius, color=color,
                                removable=removable, z_value=z_val)
        self.point_items.insert(idx, item)
        self.scene.addItem(item)

    def _add_guide_point(self, x, y):
        """Add a guide point to the path."""
        x_clamped = self._clamp(x, self.dot_radius, self._img_w - self.dot_radius)
        y_clamped = self._clamp(y, self.dot_radius, self._img_h - self.dot_radius)

        self._revert_cost_to_original()

        if not self._full_path_xy:
            self._insert_anchor_point(-1, x_clamped, y_clamped,
                                      label="", removable=True, z_val=1, radius=self.dot_radius)
        else:
            self._insert_anchor_between_subpath(x_clamped, y_clamped)

        self._apply_all_guide_points_to_cost()
        self._rebuild_full_path()

    def _insert_anchor_between_subpath(self, x_new: float, y_new: float ):
        """Insert an anchor point between existing anchor points."""        # If somehow we have no path yet
        # If somehow we have no path yet
        if not self._full_path_xy:
            self._insert_anchor_point(-1, x_new, y_new)
            return

        # Find nearest point in the current full path
        best_idx = None
        best_d2 = float('inf')
        for i, (px, py) in enumerate(self._full_path_xy):
            dx = px - x_new
            dy = py - y_new
            d2 = dx*dx + dy*dy
            if d2 < best_d2:
                best_d2 = d2
                best_idx = i

        if best_idx is None:
            self._insert_anchor_point(-1, x_new, y_new)
            return

        def approx_equal(xa, ya, xb, yb, tol=1e-3):
            """Check if two points are approximately equal."""
            return (abs(xa - xb) < tol) and (abs(ya - yb) < tol)

        def is_anchor(coord):
            """Check if a point is an anchor point."""
            cx, cy = coord
            for (ax, ay) in self.anchor_points:
                if approx_equal(ax, ay, cx, cy):
                    return True
            return False

        # Walk left
        left_anchor_pt = None
        iL = best_idx
        while iL >= 0:
            px, py = self._full_path_xy[iL]
            if is_anchor((px, py)):
                left_anchor_pt = (px, py)
                break
            iL -= 1

        # Walk right
        right_anchor_pt = None
        iR = best_idx
        while iR < len(self._full_path_xy):
            px, py = self._full_path_xy[iR]
            if is_anchor((px, py)):
                right_anchor_pt = (px, py)
                break
            iR += 1

        # If we can't find distinct anchors on left & right,
        # just insert before E.
        if not left_anchor_pt or not right_anchor_pt:
            self._insert_anchor_point(-1, x_new, y_new)
            return
        if left_anchor_pt == right_anchor_pt:
            self._insert_anchor_point(-1, x_new, y_new)
            return

        # Convert anchor coords -> anchor_points indices
        left_idx = None
        right_idx = None
        for i, (ax, ay) in enumerate(self.anchor_points):
            if approx_equal(ax, ay, left_anchor_pt[0], left_anchor_pt[1]):
                left_idx = i
            if approx_equal(ax, ay, right_anchor_pt[0], right_anchor_pt[1]):
                right_idx = i

        if left_idx is None or right_idx is None:
            self._insert_anchor_point(-1, x_new, y_new)
            return

        # Insert between them
        if left_idx < right_idx:
            insert_idx = left_idx + 1
        else:
            insert_idx = right_idx + 1

        self._insert_anchor_point(insert_idx, x_new, y_new, label="", removable=True,
                                  z_val=1, radius=self.dot_radius)

    # --------------------------------------------------------------------
    # COST IMAGE
    # --------------------------------------------------------------------
    def _revert_cost_to_original(self):
        if self.cost_image_original is not None:
            self.cost_image = self.cost_image_original.copy()

    def _apply_all_guide_points_to_cost(self):
        if self.cost_image is None:
            return
        for i, (ax, ay) in enumerate(self.anchor_points):
            if self.point_items[i].is_removable():
                self._lower_cost_in_circle(ax, ay, self.radius_cost_image)

    def _lower_cost_in_circle(self, x_f: float, y_f: float, radius: int):
        """Lower the cost in a circle centered at (x_f, y_f)."""
        if self.cost_image is None:
            return
        h, w = self.cost_image.shape
        row_c = int(round(y_f))
        col_c = int(round(x_f))
        if not (0 <= row_c < h and 0 <= col_c < w):
            return
        global_min = self.cost_image.min()
        r_s = max(0, row_c - radius)
        r_e = min(h, row_c + radius + 1)
        c_s = max(0, col_c - radius)
        c_e = min(w, col_c + radius + 1)
        for rr in range(r_s, r_e):
            for cc in range(c_s, c_e):
                dist = math.sqrt((rr - row_c)**2 + (cc - col_c)**2)
                if dist <= radius:
                    self.cost_image[rr, cc] = global_min

    # --------------------------------------------------------------------
    # PATH BUILDING
    # --------------------------------------------------------------------
    def _rebuild_full_path(self):
        """Rebuild the full path based on the anchor points."""
        for item in self.full_path_points:
            self.scene.removeItem(item)
        self.full_path_points.clear()
        self._full_path_xy.clear()

        if len(self.anchor_points) < 2 or self.cost_image is None:
            return

        big_xy = []
        for i in range(len(self.anchor_points) - 1):
            xA, yA = self.anchor_points[i]
            xB, yB = self.anchor_points[i + 1]
            sub_xy = self._compute_subpath_xy(xA, yA, xB, yB)
            if i == 0:
                big_xy.extend(sub_xy)
            else:
                if len(sub_xy) > 1:
                    big_xy.extend(sub_xy[1:])

        if len(big_xy) >= self._savgol_window_length:
            arr_xy = np.array(big_xy)
            smoothed = savgol_filter(
                arr_xy,
                window_length=self._savgol_window_length,
                polyorder=2,
                axis=0
            )
            big_xy = smoothed.tolist()

        self._full_path_xy = big_xy[:]

        n_points = len(big_xy)
        for i, (px, py) in enumerate(big_xy):
            fraction = i / (n_points - 1) if n_points > 1 else 0
            color = Qt.red
            if self._rainbow_enabled:
                color = self._rainbow_color(fraction)

            path_item = LabeledPointItem(px, py, label="",
                                         radius=self.path_radius,
                                         color=color,
                                         removable=False,
                                         z_value=0)
            self.full_path_points.append(path_item)
            self.scene.addItem(path_item)

        # Keep anchor labels on top
        for p_item in self.point_items:
            if p_item._text_item:
                p_item.setZValue(100)

    def _compute_subpath_xy(self, xA: float, yA: float, xB: float, yB: float):
        """Compute a subpath between two points."""
        if self.cost_image is None:
            return []
        h, w = self.cost_image.shape
        rA, cA = int(round(yA)), int(round(xA))
        rB, cB = int(round(yB)), int(round(xB))
        rA = max(0, min(rA, h - 1))
        cA = max(0, min(cA, w - 1))
        rB = max(0, min(rB, h - 1))
        cB = max(0, min(cB, w - 1))
        try:
            path_rc = find_path(self.cost_image, [(rA, cA), (rB, cB)])
        except ValueError as e:
            print("Error in find_path:", e)
            return []
        # Convert from (row, col) to (x, y)
        return [(c, r) for (r, c) in path_rc]

    def _rainbow_color(self, fraction: float):
        """Get a rainbow color."""
        hue = int(300 * fraction)
        saturation = 255
        value = 255
        return QColor.fromHsv(hue, saturation, value)

    # --------------------------------------------------------------------
    # MOUSE EVENTS
    # --------------------------------------------------------------------
    def mousePressEvent(self, event):
        """Handle mouse press events for dragging a point or adding a point."""
        if event.button() == Qt.LeftButton:
            self._mouse_pressed = True
            self._was_dragging = False
            self._press_view_pos = event.pos()

            idx = self._find_item_near(event.pos(), threshold=10)
            if idx is not None:
                self._dragging_idx = idx
                self._drag_counter = 0
                scene_pos = self.mapToScene(event.pos())
                px, py = self.point_items[idx].get_pos()
                self._drag_offset = (scene_pos.x() - px, scene_pos.y() - py)
                self.setCursor(Qt.ClosedHandCursor)
                return

        elif event.button() == Qt.RightButton:
            self._remove_point_by_click(event.pos())

        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move events for dragging a point or dragging the view"""
        if self._dragging_idx is not None:
            scene_pos = self.mapToScene(event.pos())
            x_new = scene_pos.x() - self._drag_offset[0]
            y_new = scene_pos.y() - self._drag_offset[1]

            r = self.point_items[self._dragging_idx]._r
            x_clamped = self._clamp(x_new, r, self._img_w - r)
            y_clamped = self._clamp(y_new, r, self._img_h - r)
            self.point_items[self._dragging_idx].set_pos(x_clamped, y_clamped)

            self._drag_counter += 1
            # Update path every 4 moves
            if self._drag_counter >= 4:
                self._drag_counter = 0
                self._revert_cost_to_original()
                self._apply_all_guide_points_to_cost()
                self.anchor_points[self._dragging_idx] = (x_clamped, y_clamped)
                self._rebuild_full_path()
        else:
            if self._mouse_pressed and (event.buttons() & Qt.LeftButton):
                dist = (event.pos() - self._press_view_pos).manhattanLength()
                if dist > self._drag_threshold:
                    self._was_dragging = True

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Handle mouse release events for dragging a point or adding a point."""
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton and self._mouse_pressed:
            self._mouse_pressed = False
            self.setCursor(Qt.ArrowCursor)

            if self._dragging_idx is not None:
                idx = self._dragging_idx
                self._dragging_idx = None
                self._drag_offset = (0, 0)
                newX, newY = self.point_items[idx].get_pos()
                self.anchor_points[idx] = (newX, newY)
                self._revert_cost_to_original()
                self._apply_all_guide_points_to_cost()
                self._rebuild_full_path()
            else:
                # No drag => add point
                if not self._was_dragging:
                    scene_pos = self.mapToScene(event.pos())
                    x, y = scene_pos.x(), scene_pos.y()
                    self._add_guide_point(x, y)

            self._was_dragging = False

    def _remove_point_by_click(self, view_pos: QPoint):
        """Remove a point by clicking on it."""
        idx = self._find_item_near(view_pos, threshold=10)
        if idx is None:
            return
        if not self.point_items[idx].is_removable():
            return

        self.scene.removeItem(self.point_items[idx])
        self.point_items.pop(idx)
        self.anchor_points.pop(idx)

        self._revert_cost_to_original()
        self._apply_all_guide_points_to_cost()
        self._rebuild_full_path()

    def _find_item_near(self, view_pos: QPoint, threshold=10):
        """Find the index of an item near a given position."""
        scene_pos = self.mapToScene(view_pos)
        x_click, y_click = scene_pos.x(), scene_pos.y()

        closest_idx = None
        min_dist = float('inf')
        for i, itm in enumerate(self.point_items):
            d = itm.distance_to(x_click, y_click)
            if d < min_dist:
                min_dist = d
                closest_idx = i
        if closest_idx is not None and min_dist <= threshold:
            return closest_idx
        return None

    # --------------------------------------------------------------------
    # UTILS
    # --------------------------------------------------------------------
    def _clamp(self, val, mn, mx):
        return max(mn, min(val, mx))

    def _clear_all_points(self):
        """Clear all anchor points and guide points."""
        for it in self.point_items:
            self.scene.removeItem(it)
        self.point_items.clear()
        self.anchor_points.clear()

        for p in self.full_path_points:
            self.scene.removeItem(p)
        self.full_path_points.clear()
        self._full_path_xy.clear()

    def clear_guide_points(self):
        """Clear all guide points."""
        i = 0
        while i < len(self.anchor_points):
            if self.point_items[i].is_removable():
                self.scene.removeItem(self.point_items[i])
                del self.point_items[i]
                del self.anchor_points[i]
            else:
                i += 1

        for it in self.full_path_points:
            self.scene.removeItem(it)
        self.full_path_points.clear()
        self._full_path_xy.clear()

        self._revert_cost_to_original()
        self._apply_all_guide_points_to_cost()
        self._rebuild_full_path()

    def get_full_path_xy(self):
        """Returns the entire path as a list of (x, y) coordinates."""
        return self._full_path_xy