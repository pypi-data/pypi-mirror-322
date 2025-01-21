from skimage.filters import gaussian
from skimage import exposure


def preprocess_image(image: "np.ndarray", sigma: int = 3, clip_limit: float = 0.01) -> "np.ndarray":
    """
    Preprocess the input image by applying histogram equalization and Gaussian smoothing.

    Args:
        image: (ndarray): Input image to be processed.
        sigma: (float, optional): Standard deviation for Gaussian kernel. Default is 3.
        clip_limit: (float, optional): Clipping limit for contrast enhancement. Default is 0.01.
    Returns:
    ndarray: The preprocessed image.
    """
    # Applies histogram equalization to enhance contrast
    image_contrasted = exposure.equalize_adapthist(
        image, clip_limit=clip_limit)

    # Applies smoothing
    smoothed_img = gaussian(image_contrasted, sigma=sigma)

    return smoothed_img
