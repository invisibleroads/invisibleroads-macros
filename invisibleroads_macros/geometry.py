from copy import copy


def flip_geometry_coordinates(geometries):
    flipped_geometries = []
    for geometry in geometries:
        if hasattr(geometry, 'geoms'):
            flipped_geometry = geometry.__class__(
                flip_geometry_coordinates(geometry.geoms))
        else:
            flipped_geometry = copy(geometry)
            flipped_geometry.coords = [flip_xy(xyz) for xyz in geometry.coords]
        flipped_geometries.append(flipped_geometry)
    return flipped_geometries


def flip_xy(xyz):
    'Flip x and y coordinates whether or not there is a z-coordinate'
    xyz = list(xyz)  # Preserve original
    xyz[0], xyz[1] = xyz[1], xyz[0]
    return xyz
