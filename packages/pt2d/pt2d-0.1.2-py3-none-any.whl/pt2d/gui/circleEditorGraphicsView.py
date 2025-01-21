from PyQt5.QtWidgets import QGraphicsView, QWidget
from .panZoomGraphicsView import PanZoomGraphicsView
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent, QWheelEvent
from .draggableCircleItem import DraggableCircleItem
from typing import Optional

# A specialized PanZoomGraphicsView for the circle editor (disk size calibration)
class CircleEditorGraphicsView(PanZoomGraphicsView):
    def __init__(self, circle_editor_widget, parent: Optional[QWidget] = None):
        """
        Constructor.
        """
        super().__init__(parent)
        self._circle_editor_widget = circle_editor_widget

    def mousePressEvent(self, event: QMouseEvent):
        """
        If the user clicks on the circle, we let the circle item handle the event.
        """
        if event.button() == Qt.LeftButton:
            # Check if user clicked on the circle item
            clicked_item = self.itemAt(event.pos())
            if clicked_item is not None:
                # climb up parent chain
                it = clicked_item
                while it is not None and not hasattr(it, "boundingRect"):
                    it = it.parentItem()

                if isinstance(it, DraggableCircleItem):
                    # Let normal item-dragging occur, no pan
                    return QGraphicsView.mousePressEvent(self, event)
        super().mousePressEvent(event)

    def wheelEvent(self, event: QWheelEvent):
        """
        If the user scrolls the mouse wheel over the circle, we change the circle
        """
        pos_in_widget = event.pos()
        item_under = self.itemAt(pos_in_widget)
        if item_under is not None:
            it = item_under
            while it is not None and not hasattr(it, "boundingRect"):
                it = it.parentItem()

            if isinstance(it, DraggableCircleItem):
                delta = event.angleDelta().y()
                step = 1 if delta > 0 else -1
                old_r = it.radius()
                new_r = max(1, old_r + step)
                it.set_radius(new_r)
                self._circle_editor_widget.update_slider_value(new_r)
                event.accept()
                return

        super().wheelEvent(event)