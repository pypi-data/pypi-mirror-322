import numpy as np
from numba import cuda, int32, float32, jit, prange
import math

from typing import Tuple

from .helper.Helperfunctions import * 


### cuda kernel ###

@cuda.jit
def initialize_search_kernel(mask: np.ndarray, start_points:np.ndarray, distances: np.ndarray, rows: int32, cols: int32):
    """
    Initialize the distances array for the BFS algorithm.
    This function is executed on the GPU.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        start_points (np.ndarray): A 2D array representing the start points (1: start point, 0: not a start point).
        distances (np.ndarray): A 2D array to store the distances from the start points.
        rows (int32): Number of rows in the grid.
        cols (int32): Number of columns in the grid.

    Returns:
        None (None):
        The distances array is modified in-place.
    """
    x, y = cuda.grid(2)
    if x < rows and y < cols:
        if mask[x, y] == 0:  # Valid cell
            distances[x, y] = 0.0 if start_points[x, y] == 1 else float('inf')
        else:
            distances[x, y] = -1  # Invalid cell

@cuda.jit
def bfs_multi_kernel(mask: np.array, distances: np.ndarray, rows: int32, cols: int32, changed: np.ndarray):
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.
    This function is executed on the GPU.

    Args:
        mask (np.ndarray): A 2D array representing the mask with obstacles (0: valid, 1: obstacle).
        distances (np.ndarray): A 2D array to store the distances from the start points.
        rows (int32): Number of rows in the mask.
        cols (int32): Number of columns in the mask.
        changed (np.ndarray): A 1D array with lenght one to indicate if the distances have changed.

    Returns:
        None (None):
        The distances array is modified in-place.
        The changed array is updated to indicate if the distances have changed.
    """
    x, y = cuda.grid(2)
    orthogonal_cost = 1.0
    diagonal_cost = 1.4142135623730951
    if x < rows and y < cols and mask[x, y] == 0:
        current_dist = distances[x, y]
        if current_dist > 0:  # Not a starting point or obstacle
            min_dist = current_dist
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if dx == 0 and dy == 0:
                        continue
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < rows and 0 <= ny < cols and mask[nx, ny] == 0:
                        neighbor_dist = distances[nx, ny]
                        if neighbor_dist >= 0:
                            cost = orthogonal_cost if (dx == 0 or dy == 0) else diagonal_cost
                            min_dist = min(min_dist, neighbor_dist + cost)

            if min_dist < current_dist:
                distances[x, y] = min_dist
                changed[0] = 1

def bfs_multi_cuda(mask: np.ndarray, start_points: np.ndarray, threads_per_block=(32, 32), max_iterations: int32=1000):
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.
    This function is executed on the GPU.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        start_points (np.ndarray): A 2D array representing the start points (1: start point, 0: not a start point).
        block_size (int32): The block size for the CUDA kernel.
        max_iterations (int32): The maximum number of iterations for the BFS algorithm.

    Returns:
        distances (np.ndarray): A 2D array representing the distances from the start points.
    """
    rows, cols = mask.shape
    distances = np.full((rows, cols), float('inf'), dtype=np.float32)

    d_grid = cuda.to_device(mask)
    d_start_points = cuda.to_device(start_points)
    d_distances = cuda.to_device(distances)

    blocks_per_grid_x = (rows + threads_per_block[0] - 1) // threads_per_block[0]
    blocks_per_grid_y = (cols + threads_per_block[1]  - 1) // threads_per_block[1]
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    # Initialize distances
    initialize_search_kernel[blocks_per_grid, threads_per_block](d_grid, d_start_points, d_distances, rows, cols)

    # Prepare for BFS iterations
    d_changed = cuda.to_device(np.zeros(1, dtype=np.int32))

    # BFS iterations
    for _ in range(max_iterations):
        d_changed[0] = 0
        bfs_multi_kernel[blocks_per_grid, threads_per_block](d_grid, d_distances, rows, cols, d_changed)
        if d_changed.copy_to_host()[0] == 0:
            break

    return d_distances.copy_to_host()


### cpu kernel ###

@jit(nopython=True)
def initialize_search_cpu(mask: np.ndarray, start_points: np.ndarray, distances: np.ndarray, rows: int32, cols: int32):
    """
    Initialize the distances array for the BFS algorithm.
    This function is executed on the CPU.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        start_points (np.ndarray): A 2D array representing the start points (1: start point, 0: not a start point).
        distances (np.ndarray): A 2D array to store the distances from the start points.
        rows (int32): Number of rows in the grid.
        cols (int32): Number of columns in the grid.

    Returns:
        None (None):
        The distances array is modified in-place.
    """
    for x in range(rows):
        for y in range(cols):
            if mask[x, y] == 0:  # Valid cell
                distances[x, y] = 0.0 if start_points[x, y] == 1 else np.inf
            else:
                distances[x, y] = -1  # Invalid cell

@jit(nopython=True)
def bfs_multi_cpu_kernel(mask: np.ndarray, distances: np.ndarray, rows: int32, cols: int32):
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.
    This function is executed on the CPU in parallel.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        distances (np.ndarray): A 2D array to store the distances from the start points.
        rows (int32): Number of rows in the grid.
        cols (int32): Number of columns in the grid.

    Returns:
        None (None):
        The distances array is modified in-place.
    """
    orthogonal_cost = 1.0
    diagonal_cost = 1.4142135623730951
    changed = False
    for x in prange(rows):
        for y in prange(cols):
            if mask[x, y] == 0:
                current_dist = distances[x, y]
                if current_dist > 0:  # Not a starting point or obstacle
                    min_dist = current_dist
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if dx == 0 and dy == 0:
                                continue
                            nx, ny = x + dx, y + dy
                            if 0 <= nx < rows and 0 <= ny < cols and mask[nx, ny] == 0:
                                neighbor_dist = distances[nx, ny]
                                if neighbor_dist >= 0:
                                    cost = orthogonal_cost if (dx == 0 or dy == 0) else diagonal_cost
                                    min_dist = min(min_dist, neighbor_dist + cost)

                    if min_dist < current_dist:
                        distances[x, y] = min_dist
                        changed = True
    return changed

@jit(nopython=True)
def bfs_multi_cpu(mask: np.ndarray, distances: np.ndarray, rows: int32, cols: int32, max_iterations: int32):
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.
    This function is executed on the CPU in a loop.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        distances (np.ndarray): A 2D array to store the distances from the start points.
        rows (int32): Number of rows in the grid.
        cols (int32): Number of columns in the grid.
        max_iterations (int32): The maximum number of iterations for the BFS algorithm.

    Returns:
        None (None):
        The distances array is modified in-place.
    """
    for _ in range(max_iterations):
        changed = bfs_multi_cpu_kernel(mask, distances, rows, cols)
        if not changed:
            break

def bfs_multi_cpu_wrapper(mask: np.ndarray, start_points: np.ndarray, max_iterations: int32=1000):
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.
    This function is executed on the CPU.

    Args:
        mask (np.ndarray): A 2D array representing the grid with obstacles (0: valid, 1: obstacle).
        start_points (np.ndarray): A 2D array representing the start points (1: start point, 0: not a start point).
        max_iterations (int32): The maximum number of iterations for the BFS algorithm. Defaults to 1000.

    Returns:
        distances (np.ndarray): A 2D array representing the distances from the start points.
    """
    rows, cols = mask.shape
    distances = np.full((rows, cols), np.inf, dtype=np.float32)

    # Initialize distances
    initialize_search_cpu(mask, start_points, distances, rows, cols)

    # BFS iterations
    bfs_multi_cpu(mask, distances, rows, cols, max_iterations)

    return distances
