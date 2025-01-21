import numpy as np
import math
from numba import cuda, int32, int16, float32, jit, prange

from typing import List, Tuple

from .helper.Helperfunctions import * 

### cuda kernel ###


@cuda.jit
def bfs_eachToEach_kernel(array: np.ndarray, max_distance: float32, result: np.ndarray) -> None:
    """
    CUDA kernel for Breadth-First Search (BFS) from each point to each in a given maximum euclidian distance on a 2D array with obstacles.
    Careful: The maximum queue length is 8192 and the local array size is 256x256. This is the maximum size the kernel can handle on a local array. with block size 32x32.
    These are hard coded in the kernel because they need to be constant to compile.
    The result is the number of visited pixels for each point.
    The algorithm walks the grid in manhatten distance.
    This function is executed on the GPU.

    Args:
        array (numpy.ndarray): The input 2D array with obstacles.
        max_distance (float): The maximum distance to travel.
        result (numpy.ndarray): The output 2D array to store the number of visited pixels for each point.

    Returns:
        None (None): The result is stored in the output array.
    """
    x, y = cuda.grid(2)
    if x >= array.shape[0] or y >= array.shape[1]:
        return

    if array[x, y] == 0:
        result[x, y] = 0
        return

    rows, cols = array.shape
    visited = cuda.local.array((256, 256), dtype=int32)
    queue = cuda.local.array((8192, 3), dtype=int32)

    for i in range(256):
        for j in range(256):
            visited[i, j] = 0

    queue_start, queue_end = 0, 1
    queue[0, 0] = x
    queue[0, 1] = y
    queue[0, 2] = 0
    visited[128, 128] = 1
    count = 1

    directions = cuda.local.array((8, 2), dtype=int32)
    directions[0] = (-1, 0)
    directions[1] = (1, 0)
    directions[2] = (0, -1)
    directions[3] = (0, 1)
    directions[4] = (-1, -1)
    directions[5] = (-1, 1)
    directions[6] = (1, -1)
    directions[7] = (1, 1)

    while queue_start < queue_end and queue_start < 8192:
        cx = queue[queue_start, 0]
        cy = queue[queue_start, 1]
        current_distance = queue[queue_start, 2]
        queue_start += 1

        for i in range(8):
            dx = directions[i, 0]
            dy = directions[i, 1]
            nx = cx + dx
            ny = cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                local_x = nx - x + 128
                local_y = ny - y + 128
                if 0 <= local_x < 256 and 0 <= local_y < 256:
                    if visited[local_x, local_y] == 0 and array[nx, ny] == 1:

                        if dx != 0 and dy != 0:
                            new_distance = current_distance + 1.414
                        else:
                            new_distance = current_distance + 1

                        if new_distance <= max_distance:
                            visited[local_x, local_y] = 1
                            count += 1
                            if queue_end < 8192:
                                queue[queue_end, 0] = nx
                                queue[queue_end, 1] = ny
                                queue[queue_end, 2] = new_distance
                                queue_end += 1
                        else:
                            queue_start = queue_end
                            break

    result[x, y] = count


def run_bfs_cuda(
    array: np.ndarray,
    max_distance: float,
    threads_per_block: Tuple[int, int] = (32, 32),
):
    """
    Runs the Breadth-First Search (BFS) kernel on the GPU.

    Args:
        array (numpy.ndarray): The input 2D array with obstacles.
        max_distance (float): The maximum distance to travel.
        threads_per_block (tuple): The number of threads per block. Default is (4, 4).

    Returns:
        result (numpy.ndarray): The output 2D array with the number of visited pixels for each point.
    """
    result = np.zeros_like(array, dtype=np.int32)
    d_array = cuda.to_device(array)
    d_result = cuda.to_device(result)

    blocks_per_grid_x = math.ceil(array.shape[0] / threads_per_block[0])
    blocks_per_grid_y = math.ceil(array.shape[1] / threads_per_block[1])
    blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

    bfs_eachToEach_kernel[blocks_per_grid, threads_per_block](
        d_array, max_distance, d_result
    )

    result = d_result.copy_to_host()
    return result


### cpu kernel ###


@jit(nopython=True)
def bfs_eachToEach_cpu_single(array: np.ndarray, max_distance: float32, x: int, y: int):
    """
    CPU function for Breadth-First Search (BFS) from each point to each in a given maximum euclidian distance on a 2D array with obstacles.
    The result is the number of visited pixels for each point.
    The algorithm walks the grid in manhatten distance.
    This function is executed on the CPU.

    Args:
        array (numpy.ndarray): The input 2D array with obstacles.
        max_distance (float): The maximum distance to travel.
        x (int): The x-coordinate of the starting point.
        y (int): The y-coordinate of the starting point.

    Returns:
        visited (int): The number of visited pixels for the starting point.
    """
    rows, cols = array.shape
    if array[x, y] == 0:
        return 0

    halfx, halfy = (int(256 / 2), int(256 / 2))
    max_size = rows * cols

    visited = np.zeros((rows, cols), dtype=np.int32)
    queue = np.zeros((max_size, 3), dtype=np.int32)
    queue_start, queue_end = 0, 1
    queue[0, 0] = x
    queue[0, 1] = y
    queue[0, 2] = 0  # Initial distance is 0
    visited[halfx, halfy] = 1  # Center of the local array
    count = 1

    directions = np.array(
        [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)],
        dtype=np.int32,
    )

    while queue_start < queue_end and queue_start < max_size:
        cx, cy, current_distance = queue[queue_start]
        queue_start += 1

        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                local_x, local_y = nx - x + halfx, ny - y + halfy
                if 0 <= local_x < rows and 0 <= local_y < cols:
                    if visited[local_x, local_y] == 0 and array[nx, ny] == 1:

                        if dx != 0 and dy != 0:
                            new_distance = current_distance + 1.414
                        else:
                            new_distance = current_distance + 1

                        if new_distance <= max_distance:
                            visited[local_x, local_y] = 1
                            count += 1
                            if queue_end < max_size:
                                queue[queue_end, 0] = nx
                                queue[queue_end, 1] = ny
                                queue[queue_end, 2] = new_distance
                                queue_end += 1
                        else:
                            queue_start = queue_end  # Stop BFS
                            break

    return count


@jit(nopython=True, parallel=True)
def bfs_cpu(array: np.ndarray, max_distance: float32):
    """
    CPU function for Breadth-First Search (BFS) from each point to each in a given maximum euclidian distance on a 2D array with obstacles.
    The result is the number of visited pixels for each point.
    The algorithm walks the grid in manhatten distance.
    This function is executed on the CPU.

    Args:
        array (numpy.ndarray): The input 2D array with obstacles.
        max_distance (float): The maximum distance to travel.

    Returns:
        numpy.ndarray: The output 2D array with the number of visited pixels for each point.
    """
    rows, cols = array.shape
    result = np.zeros_like(array, dtype=np.int32)

    for x in prange(rows):
        for y in prange(cols):
            result[x, y] = bfs_eachToEach_cpu_single(array, max_distance, x, y)

    return result

