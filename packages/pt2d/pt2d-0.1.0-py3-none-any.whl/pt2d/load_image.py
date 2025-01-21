import cv2

def load_image(path: str) -> "numpy.ndarray":
    """
    Loads an image from the specified file path in grayscale mode.

    Args:
        path (str): The file path to the image.

    Returns:
        numpy.ndarray: The loaded grayscale image.
    """
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)