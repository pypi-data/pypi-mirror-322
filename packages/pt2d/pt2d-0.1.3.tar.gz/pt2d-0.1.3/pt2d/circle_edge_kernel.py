import numpy as np
from typing import Optional

def circle_edge_kernel(k_size: int = 5, radius: Optional[int] = None) -> np.ndarray:
    """
    Create a k_size x k_size array whose values increase linearly
    from 0 at the center to 1 at the circle boundary (radius).

    Args:
        k_size: The size (width and height) of the kernel array.
        radius: The circle's radius. By default, set to (k_size-1)/2.

    Returns:
        kernel: The circle-edge-weighted kernel.
    """
    if radius is None:
        # By default, let the radius be half the kernel size
        radius = (k_size - 1) / 2

    # Create an empty kernel
    kernel = np.zeros((k_size, k_size), dtype=float)

    # Coordinates of the center
    center = radius  # same as (k_size-1)/2 if radius is default

    # Fill the kernel
    for y in range(k_size):
        for x in range(k_size):
            dist = np.sqrt((x - center)**2 + (y - center)**2)
            if dist <= radius:
                # Weight = distance / radius => 0 at center, 1 at boundary
                kernel[y, x] = dist / radius

    return kernel