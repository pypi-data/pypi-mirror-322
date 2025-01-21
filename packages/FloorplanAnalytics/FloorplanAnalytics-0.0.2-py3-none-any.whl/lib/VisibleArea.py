import numba as nb
import numpy as np
from numba import cuda, jit, prange, int32, float32
import math

from typing import Tuple

from .helper.Helperfunctions import * 

### cuda kernel ###


@cuda.jit(device=True)
def bresenham_ray_cuda(
    x0: int32,
    y0: int32,
    x1: int32,
    y1: int32,
    stop_array: np.ndarray,
    max_distance: float32,
    shape: tuple,
) -> Tuple[int32, int32]:
    """
    CUDA kernel for performing bresenham's line based raycasting.
    This function is executed on the GPU.

    Args:
        x0 (int32): The starting x-coordinate.
        y0 (int32): The starting y-coordinate.
        x1 (int32): The ending x-coordinate.
        y1 (int32): The ending y-coordinate.

        Returns:
        hit_coordinate (Tuple[int32, int32]): The hit x and y coordinates of the ray.
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    x, y = x0, y0
    distance = 0
    last_x, last_y = x0, y0

    while distance <= max_distance:
        if 0 <= x < shape[1] and 0 <= y < shape[0]:
            if stop_array[y, x] != 0:
                break
            last_x, last_y = x, y
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
            distance += 1 if dy <= dx else math.sqrt(2) / 2
        if e2 < dx:
            err += dx
            y += sy
            distance += 1 if dx < dy else math.sqrt(2) / 2

    return last_x, last_y


@cuda.jit
def raycast_and_area_cuda(
    mask: np.ndarray, num_rays: int32, max_distance: float32, area_output: np.ndarray
) -> None:
    """
    CUDA kernel for performing bresenham's line based raycasting in all directions and calculating the area between the endpoints of the rays.
    This function is executed on the GPU.

        Args:
        mask (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        num_rays (int32): The number of rays to be cast from each pixel.
        max_distance (float32): The maximum distance that the rays can travel.
        area_output (np.ndarray): A 2D array to store the area for each pixel.

    Returns:
        None (None):
        The area is stored in the area_output array.
    """
    x, y = cuda.grid(2)
    if x < area_output.shape[1] and y < area_output.shape[0]:
        ray_endpoints = cuda.local.array((1440, 2), dtype=nb.int32)

        for i in range(num_rays):
            angle = 2 * math.pi * i / num_rays
            end_x = int(x + max_distance * math.cos(angle))
            end_y = int(y + max_distance * math.sin(angle))
            last_x, last_y = bresenham_ray_cuda(
                x, y, end_x, end_y, mask, max_distance, mask.shape
            )
            ray_endpoints[i, 0] = last_x - x
            ray_endpoints[i, 1] = last_y - y

        area = 0.0
        for i in range(num_rays):
            j = (i + 1) % num_rays
            area += ray_endpoints[i, 0] * ray_endpoints[j, 1]
            area -= ray_endpoints[j, 0] * ray_endpoints[i, 1]
        area = abs(area) / 2.0

        area_output[y, x] = area


### cpu kernel ###


@jit(nopython=True)
def bresenham_ray_cpu(
    x0: int32,
    y0: int32,
    x1: int32,
    y1: int32,
    stop_array: np.ndarray,
    max_distance: float32,
    shape: tuple,
) -> Tuple[int32, int32]:
    """
    CPU function for calculating bresenham's line based raycasting.
    This function is executed on the CPU in parallel.

    Args:
        x0 (int32): The starting x-coordinate.
        y0 (int32): The starting y-coordinate.
        x1 (int32): The ending x-coordinate.
        y1 (int32): The ending y-coordinate
        stop_array (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        max_distance (float32): The maximum distance that the rays can travel.
        shape (tuple): The shape of the input mask.

    Returns:
        hit_coordinate (Tuple[int32, int32]): 
        The hit x and y coordinates of the ray.
    """
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = int32(1) if x0 < x1 else int32(-1)
    sy = int32(1) if y0 < y1 else int32(-1)
    err = dx - dy

    x, y = x0, y0
    distance = float32(0.0)
    last_x, last_y = x0, y0

    while distance <= max_distance:
        if int32(0) <= x < int32(shape[1]) and int32(0) <= y < int32(shape[0]):
            if stop_array[int32(y), int32(x)] != 0:
                break
            last_x, last_y = x, y
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
            distance += float32(1.0) if dy <= dx else float32(np.sqrt(2.0) / 2.0)
        if e2 < dx:
            err += dx
            y += sy
            distance += float32(1.0) if dx < dy else float32(np.sqrt(2.0) / 2.0)

    return last_x, last_y


@jit(nopython=True)
def calculate_area_cpu(ray_endpoints: np.ndarray) -> float32:
    """
    CPU function for calculating the area between the endpoints of the rays.
    This function is executed on the CPU in parallel.

    Args:
        ray_endpoints (np.ndarray): A 2D array representing the endpoints of the rays.

    Returns:
        area (float32): 
        The area between the endpoints of the rays.
    """
    area = float32(0.0)
    n = ray_endpoints.shape[0]
    for i in range(n):
        j = (i + 1) % n
        area += float32(ray_endpoints[i, 0] * ray_endpoints[j, 1])
        area -= float32(ray_endpoints[j, 0] * ray_endpoints[i, 1])
    return abs(area) / float32(2.0)


@jit(nopython=True, parallel=True)
def raycast_and_area_cpu(
    mask: np.ndarray, num_rays: int32, max_distance: float32, area_output: np.ndarray
) -> None:
    """
    CPU function for performing bresenham's line based raycasting in all directions and calculating the area between the endpoints of the rays.
    This function is executed on the CPU in parallel.

    Args:
        mask (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        num_rays (int32): The number of rays to be cast from each pixel.
        max_distance (float32): The maximum distance that the rays can travel.
        area_output (np.ndarray): A 2D array to store the visibility area for each pixel.

    Returns:
        None (None):
        The area is stored in the area_output array.
    """
    shape = mask.shape
    for y in prange(shape[0]):
        for x in prange(shape[1]):
            ray_endpoints = np.zeros((num_rays, 2), dtype=np.int32)
            for i in range(num_rays):
                angle = float32(2.0 * np.pi * i / num_rays)
                end_x = int32(x + max_distance * np.cos(angle))
                end_y = int32(y + max_distance * np.sin(angle))
                last_x, last_y = bresenham_ray_cpu(
                    int32(x), int32(y), end_x, end_y, mask, max_distance, shape
                )
                ray_endpoints[i, 0] = last_x - x
                ray_endpoints[i, 1] = last_y - y
            area_output[y, x] = calculate_area_cpu(ray_endpoints)
