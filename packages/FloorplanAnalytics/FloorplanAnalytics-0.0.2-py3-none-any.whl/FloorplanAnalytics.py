import numpy as np
import numba
from numba import cuda, prange, int32, float32

from typing import Tuple
from PIL import Image

from lib.helper.Helperfunctions import *
from lib.helper.Colorhelper import *


# eventually only expose the functions that are needed below for PyPI package
from lib.Floodfill import *    
from lib.GeodesicDistanceMulti import *
from lib.GeodesicRange import *
from lib.SignedDistance import *
from lib.StepDepth import *
from lib.VisibleArea import *
from lib.VisibleObstacle import *



def run_floodFill(image: np.ndarray, start_coords: Tuple[int, int], new_color: np.ndarray, tolerance: int32, use_cuda: bool=False) -> Tuple[np.ndarray, np.ndarray]:
    """
        Wrapper function for flood fill algorithm.
        This function is executed on the CPU or GPU depending on the availability of CUDA.
        
        Parameters:
        image (np.ndarray): 3D NumPy array representing the image.
        start_coords (np.ndarray): Tuple representing the starting coordinates (x, y).
        new_color (np.ndarray): 1D NumPy array representing the new color.
        tolerance (int32): Integer representing the tolerance for color difference.
        use_cuda (bool): Whether to use the CUDA GPU. Default is False.
            
        Returns:
        Modified 3D NumPy array representing the image and 2D NumPy array representing the mask.
        
    """
    if not isinstance(image, np.ndarray) or image.ndim != 3:
        raise ValueError("Input must be a 3D NumPy array")

    
    if cuda.is_available() and use_cuda:
        print("CUDA is available. Using GPU implementation.")
        return flood_fill_cuda(image, start_coords, new_color, tolerance)
    else:
        print("Using CPU parallel implementation.")
        return flood_fill_cpu(image, start_coords, new_color, tolerance)


def run_geodesicDistance(mask: np.ndarray, 
                            start_points: np.ndarray, 
                            resize_for_compute:bool=False,
                            max_size:int=1024,
                            threads_per_block: Tuple[int, int]=(32, 32), 
                            max_iterations:int=1000, 
                            use_cuda:bool=True
                            ) -> np.ndarray:
    """
    Perform the Breadth-First Search (BFS) algorithm on a grid with multiple start points.

    Args:
        mask (np.ndarray): The input 2D array with obstacles.
        start_points (np.ndarray): The input 2D array with start points.
        threads_per_block (Tuple[int, int], optional): A tuple representing the number of threads per block. Defaults to (32, 32).
        max_iterations (int, optional): The maximum number of iterations for the BFS algorithm. Defaults to 1000.
        use_cuda (bool, optional): Whether to use the CUDA GPU. Defaults to True.

    Returns:
        np.ndarray: The output 2D array with the geodesic distances from the start points.
    """
    original_shape = mask.shape
    
    #scale array before computation
    if resize_for_compute:
        mask = resize_array(mask, max_size, rescale_by_larger=True)
        start_points = resize_array(start_points, max_size, rescale_by_larger=True)
        print(f"Resized compute array from shape {original_shape} to shape: {mask.shape}")
        
    #perform computation
    if cuda.is_available() and use_cuda:
        print("CUDA is available. Using CUDA for computation")
        result = bfs_multi_cuda(mask, start_points, threads_per_block, max_iterations)
    else:
        print("CUDA not available. Using CPU with Numba")
        result = bfs_multi_cpu_wrapper(mask, start_points, max_iterations)
    
    #rescale array after computation
    if resize_for_compute:
        result = resize_array_xy(result, original_shape) 
        result = result *  max(original_shape) / max_size

    return result


def run_geodesicRange(
    array: np.ndarray,
    max_distance: float32,
    resize_for_compute:bool=False,
    max_size:int=1024,
    threads_per_block=(32, 32),
    use_cuda: bool = True,
):
    """
    Runs the Breadth-First Search (BFS) kernel on the GPU if available, otherwise on
    the CPU.
    The result is the number of visited pixels for each point.
    The algorithm walks the grid in euclidean manhattan distance.

    Args:
        array (numpy.ndarray): The input 2D array with obstacles.
        max_distance (float): The maximum distance to travel.
        threads_per_block (tuple): The number of threads per block. Default is (4, 4).
        use_cuda (bool): Whether to use the CUDA GPU. Default is True.

    Returns:
        result (numpy.ndarray): The output 2D array with the number of visited pixels for each point.
    """
    array = np.abs(array - 1)
    original_shape = array.shape
    
    #scale array before computation
    if resize_for_compute:
        array = resize_array(array, max_size)
        max_distance = max_distance * max_size / max(original_shape)
        print(f"Resized compute array from shape {original_shape} to shape: {array.shape}")

        
    # perform computation
    if cuda.is_available() and use_cuda:
        print("Using CUDA GPU")
        if threads_per_block[0] > 32 or threads_per_block[0] > 32:
            print(
                "There can't be more than 32 threads per block for this implementation. Using default (32, 32)"
            )
            result = run_bfs_cuda(array, max_distance)
        else:
            result = run_bfs_cuda(array, max_distance, threads_per_block)
    else:
        print("CUDA GPU not available. Using CPU with Numba")
        result =  bfs_cpu(array, max_distance)

    #rescale array after computation
    if resize_for_compute:
        result = resize_array_xy(result, original_shape) 
        result = result * (max(original_shape) / max_size)**2
        
    return result


def run_signedDistance(mask: np.ndarray, 
                                reference: np.ndarray, 
                                resize_for_compute: bool=False,
                                max_size: int=1024,
                                threads_per_block: Tuple[int, int]=(16, 16), 
                                use_cuda: bool=True
                                ) -> np.ndarray:
    """
    Wrapper function for calculating the signed distance field.
    This function is executed on the CPU or GPU depending on the availability of CUDA.


    Args:
        mask (np.array): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        reference (np.array): A 2D array representing the reference points to calculate the distance from.
        blocks (Tuple[int, int]): A tuple representing the number of blocks in the grid if using CUDA.
        use_cuda (bool): A boolean indicating whether to use CUDA for computation

    Returns:
        result (np.array): 
        A 2D array representing the signed distance field.
    """
    # Ensure inputs are numpy arrays
    mask = np.array(mask, dtype=np.int32)
    reference = np.array(reference, dtype=np.int32)

    
    original_shape = mask.shape
    
    #scale array before computation
    if resize_for_compute:
        mask = resize_array(mask, max_size)
        reference = resize_array(reference, max_size)
        print(f"Resized compute array from shape {original_shape} to shape: {mask.shape}")

    # Perform computation
    if cuda.is_available() and use_cuda:
        print("CUDA is available. Using CUDA for computation")
        result = cuda_signed_distance_function(mask, reference, threads_per_block)
    else:
        print("CUDA not available. Using CPU with Numba (parallel)")
        result =  cpu_signed_distance_function(mask, reference)

    #rescale array after computation
    if resize_for_compute:
        result = resize_array_xy(result, original_shape)
        result = result * max(original_shape) / max_size
        
    return result


def run_stepDepth(
    obstacle_array: np.ndarray,
    start_positions: np.ndarray,
    max_iterations: int,
    resize_for_compute: bool = False,
    max_size: int = 1024,
    threads_per_block: Tuple[int, int] = (8, 8),
    use_cuda: bool = True,
) -> np.ndarray:
    """
    Perform iterative raycasting with expanding frontier.
    This algorithm is used to calculate the visible step depth from given starting positions.
    This can give a sense of the visible depth of the environment from given points.
    It can be executed on CPU or GPU using CUDA.

    Args:
        obstacle_array (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        start_positions (np.ndarray): A 2D array of initial starting positions, each row containing [x, y] coordinates.
        max_iterations (int): Maximum number of iterations to perform.
        use_cuda (bool): Whether to use CUDA for GPU acceleration.

    Returns:
        np.ndarray: A 2D array with raycast results (0: not visible, 1+: iteration when became visible).
    """
    original_shape = obstacle_array.shape
    
    #scale array before computation
    if resize_for_compute:
        obstacle_array = resize_array(obstacle_array, max_size)
        start_positions = [scale_coordinates(point, max(original_shape), max(obstacle_array.shape)) for point in start_positions]
        print(f"Resized compute array from shape {original_shape} to shape: {obstacle_array.shape}")
    
    # Perform computation
    if use_cuda and cuda.is_available():
        print("CUDA is available. Using CUDA for computation")
        result = gpu_iterative_raycast(
            obstacle_array, start_positions, max_iterations, threads_per_block
        )
    else:
        print("CUDA not available. Using CPU with Numba (parallel)")
        result = cpu_iterative_raycast(obstacle_array, start_positions, max_iterations)

    if resize_for_compute:
        result = resize_array_xy(result, original_shape)
        
    return result


def run_visibleArea(
    obstacle_array: np.ndarray,
    max_distance: float,
    num_rays: int = 360,
    resize_for_compute: bool = False,  
    max_size: int = 1024,
    threads_per_block=(16, 16),
    use_cuda: bool = True,
) -> np.ndarray:
    """
    Wrapper function for performing bresenham's line based raycasting in all directions and calculating the area between the endpoints of the rays.
    This function is executed on the CPU or GPU depending on the availability of CUDA.

    Args:
        obstacle_array (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        num_rays (int): The number of rays to be cast from each pixel.
        max_distance (float): The maximum distance that the rays can travel.
        resize_for_compute (bool): Whether to resize the input arrays for the computation.
        max_size (int): An integer representing the maximum side length for resizing the input arrays. Default is 1024.
        threads_per_block (tuple): A tuple representing the number of threads per block. Default is (16, 16).
        use_cuda (bool): Whether to use the CUDA GPU. Default is True.

        Returns:
        result (np.ndarray): 
        A 2D array representing the visibility area for each pixel.
    """
    original_shape = obstacle_array.shape
    
    if resize_for_compute:
        obstacle_array = resize_array(obstacle_array, max_size, rescale_by_larger=True)
        max_distance = max_distance * max_size / max(original_shape)
        print(f"Resized compute array from shape {original_shape} to shape: {obstacle_array.shape}")

    
    #scale array before computation
    shape = obstacle_array.shape
    area_output = np.zeros(shape, dtype=np.float32)
    
    #perform computation
    if cuda.is_available() and use_cuda:
        print("CUDA is available. Using CUDA for computation")
        obstacle_array_gpu = cuda.to_device(obstacle_array)
        area_output_gpu = cuda.to_device(area_output)

        blocks_per_grid = (
            (shape[1] + threads_per_block[0] - 1) // threads_per_block[0],
            (shape[0] + threads_per_block[1] - 1) // threads_per_block[1],
        )
        raycast_and_area_cuda[blocks_per_grid, threads_per_block](
            obstacle_array_gpu, num_rays, max_distance, area_output_gpu
        )

        area_output = area_output_gpu.copy_to_host()
    else:
        print("CUDA not available. Using CPU with Numba (parallel)")
        raycast_and_area_cpu(
            obstacle_array, int32(num_rays), float32(max_distance), area_output
        )

    #rescale array after computation
    if resize_for_compute:
        area_output = resize_array_xy(area_output, original_shape) 
        area_output = area_output * (max(original_shape) / max_size)**2
    
    return area_output


def run_visibleObstacle(stop_array: np.ndarray, 
                        target_array: np.ndarray, 
                        num_rays: int32, 
                        max_distance: float32, 
                        resize_for_compute:bool=False,
                        max_size:int=1024,
                        threads_per_block:Tuple[int, int]=(16,16), 
                        use_cuda:bool=True
                        ) -> np.ndarray:
    """
    Function for performing ray casting and hit count calculation for all pixels.
    This function is executed on the CPU or GPU.

    Args:
        stop_array (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
        target_array (np.ndarray): A 2D array representing the target points as np array where with points of interest 1 and free space as 0.
        num_rays (int32): The number of rays to be shot from each pixel.
        max_distance (float32): The maximum distance that the rays can travel.
        threads_per_block (tuple): A tuple representing the number of threads per block. Default is (16, 16).
        use_cuda (bool): Whether to use the CUDA GPU. Default is True.
    
    Returns:
        result (np.ndarray): 
        A 2D array representing the hit count for each pixel.
    """
    original_shape = stop_array.shape
    
    #scale array before computation
    if resize_for_compute:
        stop_array = resize_array(stop_array, max_size, rescale_by_larger=True)
        target_array = resize_array(target_array, max_size, rescale_by_larger=True )
        max_distance = max_distance * max_size / max(original_shape)
        print(f"Resized compute array from shape {original_shape} to shape: {stop_array.shape}")

    
    #perform computation
    if cuda.is_available() and use_cuda:
        print("CUDA is available. Using CUDA for computation")
        result = raycast_hit_count_cuda_wrapper(stop_array, target_array, num_rays, max_distance, threads_per_block)
    else:
        print("CUDA not available. Using CPU with Numba (parallel)")
        result = raycast_hit_count_cpu(stop_array, target_array, num_rays, max_distance)
    
    #rescale array after computation
    if resize_for_compute:
        result = resize_array_xy(result, original_shape) 
        
    return result
