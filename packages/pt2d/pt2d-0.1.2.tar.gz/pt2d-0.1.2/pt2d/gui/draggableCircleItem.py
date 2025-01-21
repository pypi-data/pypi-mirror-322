from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsItem
from PyQt5.QtGui import QPen, QBrush, QColor
from PyQt5.QtCore import Qt
from typing import Optional

class DraggableCircleItem(QGraphicsEllipseItem):
    """
    A QGraphicsEllipseItem that can be dragged around.
    """
    def __init__(self, x: float, y: float, radius: float = 20, color: QColor = Qt.red, parent: Optional[QGraphicsItem] = None):
        """
        Constructor.
        """
        super().__init__(0, 0, 2*radius, 2*radius, parent)
        self._r = radius

        pen = QPen(color)
        brush = QBrush(color)
        self.setPen(pen)
        self.setBrush(brush)

        # Enable item-based dragging
        self.setFlags(QGraphicsEllipseItem.ItemIsMovable |
                      QGraphicsEllipseItem.ItemIsSelectable |
                      QGraphicsEllipseItem.ItemSendsScenePositionChanges)

        # Position so that (x, y) is the center
        self.setPos(x - radius, y - radius)

    def set_radius(self, r: float):
        """
        Set the radius of the circle
        """
        old_center = self.sceneBoundingRect().center()
        self._r = r
        self.setRect(0, 0, 2*r, 2*r)
        new_center = self.sceneBoundingRect().center()
        diff_x = old_center.x() - new_center.x()
        diff_y = old_center.y() - new_center.y()
        self.moveBy(diff_x, diff_y)

    def radius(self):
        """
        Get the radius of the circle
        """
        return self._r