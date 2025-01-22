import math
from typing import List

import numpy as np

from uval.utils.log import logger


def iou(start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]) -> float:
    """Calculates the intersection over union of the two cubes A and B.

    Args:
        start_a (List[float]): bottom left corner of the cube A.
        shape_a (List[float]): size of each dimension in the cube A.
        start_b (List[float]): bottom left corner of the cube B.
        shape_b (List[float]): size of each dimension in the cube B.

    Returns:
        float: 3D IOU of these cubes.
    """

    if (
        np.any(np.array(start_a) < 0)
        or np.any(np.array(start_b) < 0)
        or np.any(np.array(shape_a) < 0)
        or np.any(np.array(shape_b) < 0)
    ):
        logger.warning(f"bounding box coordinates are negative!{start_a}{shape_a}{start_b}{shape_b}")
        return 0

    if boxes_intersect(start_a, shape_a, start_b, shape_b) is False:
        return 0
    inter_area = get_intersection_area(start_a, shape_a, start_b, shape_b)
    union = get_union_areas(start_a, shape_a, start_b, shape_b)
    # intersection over union
    iou = inter_area / union
    assert iou >= 0
    return iou


def boxes_intersect(start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]) -> bool:
    """Check if the two cubes intersect or not.

    Args:
        start_a (List[float]): bottom left corner of the cube A.
        shape_a (List[float]): size of each dimension in the cube A.
        start_b (List[float]): bottom left corner of the cube B.
        shape_b (List[float]): size of each dimension in the cube B.

    Returns:
        bool: True if the two cubes intersect. otherwise False.
    """

    if start_a[0] > start_b[0] + shape_b[0]:
        return False
    if start_b[0] > start_a[0] + shape_a[0]:
        return False
    if start_a[1] > start_b[1] + shape_b[1]:
        return False
    if start_b[1] > start_a[1] + shape_a[1]:
        return False
    if start_a[2] > start_b[2] + shape_b[2]:
        return False
    if start_b[2] > start_a[2] + shape_a[2]:
        return False
    return True


def get_union_areas(start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]) -> float:
    """Calculates the Union of the areas of the two cubes A and B.

    Args:
        start_a (List[float]): bottom left corner of the cube A.
        shape_a (List[float]): size of each dimension in the cube A.
        start_b (List[float]): bottom left corner of the cube B.
        shape_b (List[float]): size of each dimension in the cube B.

    Returns:
        float: union of the two cubes.
    """
    area_a = get_area(shape_a)
    area_b = get_area(shape_b)
    inter_area = get_intersection_area(start_a, shape_a, start_b, shape_b)
    return float(area_a + area_b - inter_area)


def get_area(shape: List[float]) -> float:
    """calculates the area of a cube.

    Args:
        shape (List[float]): size of each dimension in the cube.

    Returns:
        float: area of the cube.
    """

    return math.prod(shape)


def get_intersection_area(
    start_a: List[float], shape_a: List[float], start_b: List[float], shape_b: List[float]
) -> float:
    """Calculates the intersection of the areas of the two cubes A and B.

    Args:
        start_a (List[float]): bottom left corner of the cube A.
        shape_a (List[float]): size of each dimension in the cube A.
        start_b (List[float]): bottom left corner of the cube B.
        shape_b (List[float]): size of each dimension in the cube B.

    Returns:
        float: intersection of the two cubes.
    """
    x_a = max(start_a[0], start_b[0])
    y_a = max(start_a[1], start_b[1])
    z_a = max(start_a[2], start_b[2])
    x_b = min(start_a[0] + shape_a[0], start_b[0] + shape_b[0])
    y_b = min(start_a[1] + shape_a[1], start_b[1] + shape_b[1])
    z_b = min(start_a[2] + shape_a[2], start_b[2] + shape_b[2])
    # intersection area
    return (x_b - x_a) * (y_b - y_a) * (z_b - z_a)
