from PyQt5.QtWidgets import (
    QGraphicsScene, QGraphicsPixmapItem, QPushButton,
    QHBoxLayout, QVBoxLayout, QWidget, QSlider, QLabel
)
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt, QRectF, QSize
from .circleEditorGraphicsView import CircleEditorGraphicsView
from .draggableCircleItem import DraggableCircleItem
from typing import Optional, Callable

class CircleEditorWidget(QWidget):
    """
    A widget for the user to calibrate the disk size (kernel size) for the ridge detection.
    """
    def __init__(self, pixmap: QPixmap, init_radius: int = 20, done_callback: Optional[Callable[[], None]] = None, parent: Optional[QWidget] = None):
        """
        Constructor.
        """
        super().__init__(parent)
        self._pixmap = pixmap
        self._done_callback = done_callback
        self._init_radius = init_radius

        layout = QVBoxLayout(self)
        self.setLayout(layout)

        # Add centered label above image
        label_instructions = QLabel("Rezise the dot to match the size of the path you are trying to extract")
        label_instructions.setAlignment(Qt.AlignCenter)
        big_font = QFont("Arial", 20)
        big_font.setBold(True)
        label_instructions.setFont(big_font)
        layout.addWidget(label_instructions)

        # Show the image
        self._graphics_view = CircleEditorGraphicsView(circle_editor_widget=self)
        self._scene = QGraphicsScene(self)
        self._graphics_view.setScene(self._scene)
        layout.addWidget(self._graphics_view)

        self._image_item = QGraphicsPixmapItem(self._pixmap)
        self._scene.addItem(self._image_item)

        # Put circle in center
        cx = self._pixmap.width() / 2
        cy = self._pixmap.height() / 2
        self._circle_item = DraggableCircleItem(cx, cy, radius=self._init_radius, color=Qt.red)
        self._scene.addItem(self._circle_item)

        # Fit in view
        self._graphics_view.setSceneRect(QRectF(self._pixmap.rect()))
        self._graphics_view.fitInView(self._image_item, Qt.KeepAspectRatio)

        ### Controls below
        bottom_layout = QHBoxLayout()
        layout.addLayout(bottom_layout)

        # label + slider
        self._lbl_size = QLabel(f"size ({self._init_radius})")
        bottom_layout.addWidget(self._lbl_size)

        self._slider = QSlider(Qt.Horizontal)
        self._slider.setRange(1, 200)
        self._slider.setValue(self._init_radius)
        bottom_layout.addWidget(self._slider)

        # Done button
        self._btn_done = QPushButton("Done")
        bottom_layout.addWidget(self._btn_done)

        # Connect signals
        self._slider.valueChanged.connect(self._on_slider_changed)
        self._btn_done.clicked.connect(self._on_done_clicked)

    def _on_slider_changed(self, value: int):
        """
        Handle slider value changes.
        """
        self._circle_item.set_radius(value)
        self._lbl_size.setText(f"size ({value})")

    def _on_done_clicked(self):
        """
        Handle the user clicking the "Done" button.
        """
        final_radius = self._circle_item.radius()
        if self._done_callback is not None:
            self._done_callback(final_radius)

    def update_slider_value(self, new_radius: int):
        """
        Update the slider value.
        """
        self._slider.blockSignals(True)
        self._slider.setValue(new_radius)
        self._slider.blockSignals(False)
        self._lbl_size.setText(f"size ({new_radius})")

    def sizeHint(self):
        return QSize(800, 600)
