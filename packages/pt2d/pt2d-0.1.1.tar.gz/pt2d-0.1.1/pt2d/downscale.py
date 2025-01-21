import cv2
import numpy as np
from typing import Tuple

# Currently not implemented
def downscale(img: np.ndarray, points: Tuple[Tuple[int, int], Tuple[int, int]], scale_percent: int) -> Tuple[np.ndarray, Tuple[Tuple[int, int], Tuple[int, int]]]:
    """
    Downscale an image and its corresponding points.

    Args:
        img: The image.
        points: The points to downscale.
        scale_percent: The percentage to downscale to. E.g. scale_percent = 60 results in a new image 60% of the original image's size.

    Returns:
        The downsampled image and the downsampled points.
    """
    if scale_percent == 100:
        return img, (tuple(points[0]), tuple(points[1]))
    else:
        # Compute new dimensions
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        new_dimensions = (width, height)

        # Downsample
        downsampled_img = cv2.resize(img, new_dimensions, interpolation=cv2.INTER_AREA)

        # Scaling factors
        scale_x = width / img.shape[1]
        scale_y = height / img.shape[0]

        # Scale the points (x, y)
        seed_xy = tuple(points[0])
        target_xy = tuple(points[1])
        scaled_seed_xy = (int(seed_xy[0] * scale_x), int(seed_xy[1] * scale_y))
        scaled_target_xy = (int(target_xy[0] * scale_x), int(target_xy[1] * scale_y))

        return downsampled_img, (scaled_seed_xy, scaled_target_xy)