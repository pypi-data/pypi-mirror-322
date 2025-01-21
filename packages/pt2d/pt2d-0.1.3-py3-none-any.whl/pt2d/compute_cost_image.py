from skimage.feature import canny
from scipy.signal import convolve2d
from .compute_disk_size import compute_disk_size
from .load_image import load_image
from .preprocess_image import preprocess_image
from .circle_edge_kernel import circle_edge_kernel
import numpy as np

def compute_cost_image(path: str, user_radius: int, sigma: int = 3, clip_limit: float = 0.01) -> np.ndarray:
    """
    Compute the cost image for a given image path, user radius, and optional parameters.
    
    Args:
        path: The path to the image file.
        user_radius: The radius of the disk.
        sigma: The standard deviation for Gaussian smoothing.
        clip_limit: The limit for contrasting the image.

    Returns:
        The cost image as a NumPy array.
    """
    disk_size = compute_disk_size(user_radius)

    # Load image
    image = load_image(path)

    # Apply smoothing
    smoothed_img = preprocess_image(image, sigma=sigma, clip_limit=clip_limit)

    # Apply Canny edge detection
    canny_img = canny(smoothed_img)

    # Perform disk convolution
    binary_img = canny_img
    kernel = circle_edge_kernel(k_size=disk_size)
    convolved = convolve2d(binary_img, kernel, mode='same', boundary='fill')

    # Create cost image
    cost_img = (convolved.max() - convolved)**4  # Invert edges: higher cost where edges are stronger

    return cost_img