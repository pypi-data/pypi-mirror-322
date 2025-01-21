import numpy as np

def compute_disk_size(user_radius: int, upscale_factor: float = 1.2) -> int:
    """
    Compute the size of the disk to be used in the cost image computation.

    Args:
        user_radius: The radius in pixels.
        upscale_factor: The factor by which the disk size will be upscaled.

    Returns:
        The size of the disk.
    """
    return int(np.ceil(upscale_factor * 2 * user_radius + 1) // 2 * 2 + 1)