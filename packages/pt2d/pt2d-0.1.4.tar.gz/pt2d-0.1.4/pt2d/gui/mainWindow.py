import math
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QPushButton, QHBoxLayout, 
    QVBoxLayout, QWidget, QFileDialog
)
from PyQt5.QtGui import QPixmap, QImage, QCloseEvent
from ..compute_cost_image import compute_cost_image
from ..preprocess_image import preprocess_image
from .advancedSettingsWidget import AdvancedSettingsWidget
from .imageGraphicsView import ImageGraphicsView
from .circleEditorWidget import CircleEditorWidget

class MainWindow(QMainWindow):
    def __init__(self):
        """
        Initialize the main window for the application.

        This method sets up the main window, including the layout, widgets, and initial state.
        It initializes various attributes related to the image processing and user interface.
        """
        super().__init__()
        self.setWindowTitle("Path Tracing in 2D images")

        self._last_loaded_pixmap = None
        self._circle_calibrated_radius = 6
        self._last_loaded_file_path = None

        # Value for the contrast slider
        self._current_clip_limit = 0.01

        # Outer widget and layout
        self._main_widget = QWidget()
        self._main_layout = QHBoxLayout(self._main_widget)

        # Container for the image area and its controls
        self._left_panel = QVBoxLayout()

        # Container widget for stretching the panel
        self._left_container = QWidget()
        self._left_container.setLayout(self._left_panel)

        self._main_layout.addWidget(self._left_container, 7)  # 70% ratio of the full window
        
        # Advanced widget window
        self._advanced_widget = AdvancedSettingsWidget(self)
        self._advanced_widget.hide()
        self._main_layout.addWidget(self._advanced_widget, 3) # 30% ratio of the full window

        self.setCentralWidget(self._main_widget)

        # The image view
        self.image_view = ImageGraphicsView()
        self._left_panel.addWidget(self.image_view)

        # Button row
        btn_layout = QHBoxLayout()
        self.btn_load_image = QPushButton("Load Image")
        self.btn_load_image.clicked.connect(self.load_image)
        btn_layout.addWidget(self.btn_load_image)

        self.btn_export_path = QPushButton("Export Path")
        self.btn_export_path.clicked.connect(self.export_path)
        btn_layout.addWidget(self.btn_export_path)

        self.btn_clear_points = QPushButton("Clear Points")
        self.btn_clear_points.clicked.connect(self.clear_points)
        btn_layout.addWidget(self.btn_clear_points)

        self.btn_advanced = QPushButton("Advanced Settings")
        self.btn_advanced.setCheckable(True)
        self.btn_advanced.clicked.connect(self._toggle_advanced_settings)
        btn_layout.addWidget(self.btn_advanced)

        self._left_panel.addLayout(btn_layout)

        self.resize(1000, 600)
        self._old_central_widget = None
        self._editor = None

    def _toggle_advanced_settings(self, checked: bool):
        """
        Toggles the visibility of the advanced settings widget.
        """
        if checked:
            self._advanced_widget.show()
        else:
            self._advanced_widget.hide()
        # Force re-layout
        self.adjustSize()


    def open_circle_editor(self):
        """
        Replace central widget with circle editor.
        """
        if not self._last_loaded_pixmap:
            print("No image loaded yet! Cannot open circle editor.")
            return

        old_widget = self.takeCentralWidget()
        self._old_central_widget = old_widget

        init_radius = self._circle_calibrated_radius
        editor = CircleEditorWidget(
            pixmap=self._last_loaded_pixmap,
            init_radius=init_radius,
            done_callback=self._on_circle_editor_done
        )
        self._editor = editor
        self.setCentralWidget(editor)


    def _on_circle_editor_done(self, final_radius: int):
        """
        Updates the calibrated radius, computes the cost image based on the new radius,
        and updates the image view with the new cost image.
        It also restores the previous central widget and cleans up the editor widget.
        """
        self._circle_calibrated_radius = final_radius
        print(f"Circle Editor done. Radius = {final_radius}")

        # Update cost image and path using new radius
        if self._last_loaded_file_path:
            cost_img = compute_cost_image(
                self._last_loaded_file_path,
                self._circle_calibrated_radius,
                clip_limit=self._current_clip_limit
            )
            self.image_view.cost_image_original = cost_img
            self.image_view.cost_image = cost_img.copy()
            self.image_view._apply_all_guide_points_to_cost()
            self.image_view._rebuild_full_path()
            self._update_advanced_images()

        # Swap back to central widget
        editor_widget = self.takeCentralWidget()
        if editor_widget is not None:
            editor_widget.setParent(None)

        if self._old_central_widget is not None:
            self.setCentralWidget(self._old_central_widget)
            self._old_central_widget = None

        if self._editor is not None:
            self._editor.deleteLater()
            self._editor = None

    def toggle_rainbow(self):
        """
        Toggle rainbow coloring of the path.
        """
        self.image_view.toggle_rainbow()

    def load_image(self):
        """
        Load an image and update the image view and cost image.
        The supported image formats are: PNG, JPG, JPEG, BMP, and TIF.
        """
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "",
            "Images (*.png *.jpg *.jpeg *.bmp *.tif)",
            options=options
        )
        
        if file_path:
            self.image_view.load_image(file_path)

            cost_img = compute_cost_image(
                file_path,
                self._circle_calibrated_radius,
                clip_limit=self._current_clip_limit
            )
            self.image_view.cost_image_original = cost_img
            self.image_view.cost_image = cost_img.copy()

            pm = QPixmap(file_path)
            if not pm.isNull():
                self._last_loaded_pixmap = pm

            self._last_loaded_file_path = file_path
            self._update_advanced_images()

    def update_contrast(self, clip_limit: float):
        """
        Updates and applies the contrast value of the image.
        """
        self._current_clip_limit = clip_limit
        if self._last_loaded_file_path:
            cost_img = compute_cost_image(
                self._last_loaded_file_path,
                self._circle_calibrated_radius,
                clip_limit=clip_limit
            )
            self.image_view.cost_image_original = cost_img
            self.image_view.cost_image = cost_img.copy()
            self.image_view._apply_all_guide_points_to_cost()
            self.image_view._rebuild_full_path()

        self._update_advanced_images()

    def _update_advanced_images(self):
        """
        Updates the advanced images display with the latest image.
        If no image has been loaded, the method returns without making any updates.
        """
        if not self._last_loaded_pixmap:
            return
        pm_np = self._qpixmap_to_gray_float(self._last_loaded_pixmap)
        contrasted_blurred = preprocess_image(
            pm_np,
            sigma=3,
            clip_limit=self._current_clip_limit
        )
        cost_img_np = self.image_view.cost_image
        self._advanced_widget.update_displays(contrasted_blurred, cost_img_np)

    def _qpixmap_to_gray_float(self, qpix: QPixmap) -> np.ndarray:
        """
        Convert a QPixmap to a grayscale float array.

        Args:
            qpix: The QPixmap to be converted.

        Returns:
            A 2D numpy array representing the grayscale image.
        """
        img = qpix.toImage()
        img = img.convertToFormat(QImage.Format_ARGB32)
        ptr = img.bits()
        ptr.setsize(img.byteCount())
        arr = np.frombuffer(ptr, np.uint8).reshape((img.height(), img.width(), 4))
        rgb = arr[..., :3].astype(np.float32)
        gray = rgb.mean(axis=2) / 255.0
        return gray

    def export_path(self):
        """
        Exports the path as a CSV in the format: x, y, TYPE,
        ensuring that each anchor influences exactly one path point.
        """
        full_xy = self.image_view.get_full_path_xy()
        if not full_xy:
            print("No path to export.")
            return

        anchor_points = self.image_view.anchor_points

        # Finds the index of the closest path point for each anchor point
        user_placed_indices = set()
        for ax, ay in anchor_points:
            min_dist = float('inf')
            closest_idx = None
            for i, (px, py) in enumerate(full_xy):
                dist = math.hypot(px - ax, py - ay)
                if dist < min_dist:
                    min_dist = dist
                    closest_idx = i
            if closest_idx is not None:
                user_placed_indices.add(closest_idx)

        # Ask user for the CSV filename
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Path", "",
            "CSV Files (*.csv);;All Files (*)",
            options=options
        )
        if not file_path:
            return

        import csv
        with open(file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["x", "y", "TYPE"])

            for i, (x, y) in enumerate(full_xy):
                ptype = "USER-PLACED" if i in user_placed_indices else "PATH"
                writer.writerow([x, y, ptype])

        print(f"Exported path with {len(full_xy)} points to {file_path}")

    def clear_points(self):
        """
        Clears points from the image.
        """
        self.image_view.clear_guide_points()

    def closeEvent(self, event: QCloseEvent):
        """
        Handle the window close event.
        
        Args:
            event: The close event.
        """
        super().closeEvent(event)