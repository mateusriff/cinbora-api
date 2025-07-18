import math

def haversine_distance(coord1, coord2):
    """
    Calculate the great-circle distance between two points 
    on the Earth's surface given in decimal degrees.
    
    Parameters:
        coord1: tuple of float (lon1, lat1)
        coord2: tuple of float (lon2, lat2)
    
    Returns:
        Distance in meters as a float
    """
    # Radius of Earth in meters
    R = 6371000  
    
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    # Convert decimal degrees to radians
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    # Haversine formula
    a = math.sin(delta_phi / 2) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance