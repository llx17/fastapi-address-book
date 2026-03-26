from haversine import Unit, haversine


def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float,
) -> float:
    return haversine((lat1, lon1), (lat2, lon2), unit=Unit.KILOMETERS)