import math
from PyQt5.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem
from PyQt5.QtGui import QPen, QBrush, QColor, QFont
from PyQt5.QtCore import Qt


class LabeledPointItem(QGraphicsEllipseItem):
    """
    A QGraphicsEllipseItem subclass that represents a labeled point in a 2D space.

    This class creates a circular point.
    The point can be customized with different colors, sizes, and labels, and can
    be marked as removable.
    """

    def __init__(self, x: float, y: float, label: str ="", radius:int =4, 
                 color=Qt.red, removable=True, z_value=0, parent=None):
        super().__init__(0, 0, 2*radius, 2*radius, parent)
        self._x = x
        self._y = y
        self._r = radius
        self._removable = removable

        pen = QPen(color)
        brush = QBrush(color)
        self.setPen(pen)
        self.setBrush(brush)
        self.setZValue(z_value)

        self._text_item = None
        if label:
            self._text_item = QGraphicsTextItem(self)
            self._text_item.setPlainText(label)
            self._text_item.setDefaultTextColor(QColor("black"))
            font = QFont("Arial", 14)
            font.setBold(True)
            self._text_item.setFont(font)
            self._scale_text_to_fit()

        self.set_pos(x, y)

    def _scale_text_to_fit(self):
        """Scales the text to fit inside the circle."""
        if not self._text_item:
            return
        self._text_item.setScale(1.0)
        circle_diam = 2 * self._r
        raw_rect = self._text_item.boundingRect()
        text_w = raw_rect.width()
        text_h = raw_rect.height()
        if text_w > circle_diam or text_h > circle_diam:
            scale_factor = min(circle_diam / text_w, circle_diam / text_h)
            self._text_item.setScale(scale_factor)
        self._center_label()

    def _center_label(self):
        """Centers the text inside the circle."""
        if not self._text_item:
            return
        ellipse_w = 2 * self._r
        ellipse_h = 2 * self._r
        raw_rect = self._text_item.boundingRect()
        scale_factor = self._text_item.scale()
        scaled_w = raw_rect.width() * scale_factor
        scaled_h = raw_rect.height() * scale_factor
        tx = (ellipse_w - scaled_w) * 0.5
        ty = (ellipse_h - scaled_h) * 0.5
        self._text_item.setPos(tx, ty)

    def set_pos(self, x, y):
        """Positions the circle so its center is at (x, y)."""
        self._x = x
        self._y = y
        self.setPos(x - self._r, y - self._r)

    def get_pos(self):
        """Returns the (x, y) coordinates of the center of the circle."""
        return (self._x, self._y)

    def distance_to(self, x_other, y_other):
        """Returns the Euclidean distance from the center 
        of the circle to another circle."""
        return math.sqrt((self._x - x_other)**2 + (self._y - y_other)**2)

    def is_removable(self):
        """Returns True if the point is removable, False otherwise."""
        return self._removable
