from PyQt5.QtWidgets import QGraphicsView, QSizePolicy
from PyQt5.QtCore import Qt

class PanZoomGraphicsView(QGraphicsView):
    """
    A QGraphicsView subclass that supports panning and zooming with the mouse.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragMode(QGraphicsView.NoDrag)  # We'll handle panning manually
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self._panning = False
        self._pan_start = None

        # Expands layout
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def wheelEvent(self, event):
        """ Zoom in/out with mouse wheel. """
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor
        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)
        event.accept()

    def mousePressEvent(self, event):
        """ If left button: Start panning (unless overridden). """
        if event.button() == Qt.LeftButton:
            self._panning = True
            self._pan_start = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """ If panning, translate the scene. """
        if self._panning and self._pan_start is not None:
            delta = event.pos() - self._pan_start
            self._pan_start = event.pos()
            self.translate(delta.x(), delta.y())
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """ End panning. """
        if event.button() == Qt.LeftButton:
            self._panning = False
            self.setCursor(Qt.ArrowCursor)
        super().mouseReleaseEvent(event)
