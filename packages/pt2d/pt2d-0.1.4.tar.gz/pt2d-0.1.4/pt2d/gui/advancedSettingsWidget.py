from PyQt5.QtWidgets import (
    QPushButton, QVBoxLayout, QWidget,
    QSlider, QLabel, QGridLayout, QSizePolicy
)
from PyQt5.QtGui import QPixmap, QImage, QShowEvent
from PyQt5.QtCore import Qt
import numpy as np
from typing import Optional

class AdvancedSettingsWidget(QWidget):
    """
    Shows toggle rainbow, circle editor, line smoothing slider, contrast slider,
    plus two image previews (contrasted-blurred and cost).
    The images maintain aspect ratio upon resize.
    """
    def __init__(self, main_window, parent: Optional[QWidget] = None):
        """
        Constructor.
        """
        super().__init__(parent)
        self._main_window = main_window

        self._last_cb_pix = None   # store QPixmap for contrasted-blurred image
        self._last_cost_pix = None # store QPixmap for cost image

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # A small grid for controls
        controls_layout = QGridLayout()

        # Rainbow toggle
        self.btn_toggle_rainbow = QPushButton("Toggle Rainbow")
        self.btn_toggle_rainbow.clicked.connect(self._on_toggle_rainbow)
        controls_layout.addWidget(self.btn_toggle_rainbow, 0, 0)

        # Disk size calibration (Circle editor)
        self.btn_circle_editor = QPushButton("Calibrate Kernel Size")
        self.btn_circle_editor.clicked.connect(self._main_window.open_circle_editor)
        controls_layout.addWidget(self.btn_circle_editor, 0, 1)

        # Line smoothing slider + label
        self._lab_smoothing = QLabel("Line smoothing (22)")
        controls_layout.addWidget(self._lab_smoothing, 1, 0)
        self.line_smoothing_slider = QSlider(Qt.Horizontal)
        self.line_smoothing_slider.setRange(3, 51)
        self.line_smoothing_slider.setValue(22)
        self.line_smoothing_slider.valueChanged.connect(self._on_line_smoothing_slider)
        controls_layout.addWidget(self.line_smoothing_slider, 1, 1)

        # Contrast slider + label
        self._lab_contrast = QLabel("Contrast (0.01)")
        controls_layout.addWidget(self._lab_contrast, 2, 0)
        self.contrast_slider = QSlider(Qt.Horizontal)
        self.contrast_slider.setRange(1, 40)
        self.contrast_slider.setValue(10)  # i.e. 0.001
        self.contrast_slider.setSingleStep(1)
        self.contrast_slider.valueChanged.connect(self._on_contrast_slider)
        controls_layout.addWidget(self.contrast_slider, 2, 1)

        main_layout.addLayout(controls_layout)

        self.setMinimumWidth(350)

        # A vertical layout for the two images, each with a label above it
        images_layout = QVBoxLayout()

        # Contrasted-blurred label + image
        self.label_cb_title = QLabel("Contrasted Blurred Image")
        self.label_cb_title.setAlignment(Qt.AlignCenter)
        images_layout.addWidget(self.label_cb_title)

        self.label_contrasted_blurred = QLabel()
        self.label_contrasted_blurred.setAlignment(Qt.AlignCenter)
        self.label_contrasted_blurred.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        images_layout.addWidget(self.label_contrasted_blurred)

        # Cost image label + image
        self.label_cost_title = QLabel("Current COST IMAGE")
        self.label_cost_title.setAlignment(Qt.AlignCenter)
        images_layout.addWidget(self.label_cost_title)

        self.label_cost_image = QLabel()
        self.label_cost_image.setAlignment(Qt.AlignCenter)
        self.label_cost_image.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        images_layout.addWidget(self.label_cost_image)

        main_layout.addLayout(images_layout)

    def showEvent(self, event: QShowEvent):
        """ When shown, ask parent to resize to accommodate. """
        super().showEvent(event)
        if self.parentWidget():
            self.parentWidget().adjustSize()

    def resizeEvent(self, event: QShowEvent):
        """
        Keep the images at correct aspect ratio by re-scaling
        stored pixmaps to the new label sizes.
        """
        super().resizeEvent(event)
        self._update_labels()

    def _update_labels(self):
        """
        Re-scale stored pixmaps to the new label sizes.
        """
        if self._last_cb_pix is not None:
            scaled_cb = self._last_cb_pix.scaled(
                self.label_contrasted_blurred.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_contrasted_blurred.setPixmap(scaled_cb)

        if self._last_cost_pix is not None:
            scaled_cost = self._last_cost_pix.scaled(
                self.label_cost_image.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.label_cost_image.setPixmap(scaled_cost)

    def _on_toggle_rainbow(self):
        """
        Called when the rainbow toggle button is clicked.
        """
        self._main_window.toggle_rainbow()

    def _on_line_smoothing_slider(self, value: int):
        """
        Called when the line smoothing slider is moved.
        """
        self._lab_smoothing.setText(f"Line smoothing ({value})")
        self._main_window.image_view.set_savgol_window_length(value)

    def _on_contrast_slider(self, value: int):
        """
        Called when the contrast slider is moved.
        """
        clip_limit = value / 1000
        self._lab_contrast.setText(f"Contrast ({clip_limit:.3f})")
        self._main_window.update_contrast(clip_limit)

    def update_displays(self, contrasted_img_np: np.ndarray, cost_img_np: np.ndarray):
        """
        Update the contrasted-blurred and cost images.
        """
        cb_pix = self._np_array_to_qpixmap(contrasted_img_np)
        cost_pix = self._np_array_to_qpixmap(cost_img_np, normalize=True)

        self._last_cb_pix = cb_pix
        self._last_cost_pix = cost_pix
        self._update_labels()

    def _np_array_to_qpixmap(self, arr: np.ndarray, normalize: bool = False) -> QPixmap:
        """
        Convert a numpy array to a QPixmap.
        """
        if arr is None:
            return None
        arr_ = arr.copy()
        if normalize:
            mn, mx = arr_.min(), arr_.max()
            if abs(mx - mn) < 1e-12:
                arr_[:] = 0
            else:
                arr_ = (arr_ - mn) / (mx - mn)
        arr_ = np.clip(arr_, 0, 1)
        arr_255 = (arr_ * 255).astype(np.uint8)

        h, w = arr_255.shape
        qimage = QImage(arr_255.data, w, h, w, QImage.Format_Grayscale8)
        return QPixmap.fromImage(qimage)
