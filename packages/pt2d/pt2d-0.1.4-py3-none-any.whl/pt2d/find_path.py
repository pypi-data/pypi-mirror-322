from skimage.graph import route_through_array

def find_path(cost_image, points):

    if len(points) != 2:
        raise ValueError("Points should be a list of 2 points: seed and target.")
    
    seed_rc, target_rc = points

    path_rc, cost = route_through_array(
        cost_image, 
        start=seed_rc, 
        end=target_rc, 
        fully_connected=True
    )

    return path_rc