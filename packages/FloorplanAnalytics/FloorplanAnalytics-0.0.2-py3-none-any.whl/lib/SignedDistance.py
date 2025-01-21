import numpy as np
import numba as nb
from numba import cuda, float32, int32, njit, prange
import math
from typing import Tuple

from .helper.Helperfunctions import * 

### cuda kernel ###

@cuda.jit
def cuda_signed_distance_function_kernel(mask: np.ndarray, reference: np.ndarray, output: np.ndarray) -> None:
  """
  CUDA kernel for calculating the signed distance field.
  This function is executed on the GPU.

  Args:
    mask (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
    reference (np.ndarray): A 2D array representing the reference points to calculate the distance from.
    output (np.ndarray): A 2D array to store the signed distance field.

  Returns:
    None (None):
    The function modifies the output array in-place.
  """
  x, y = cuda.grid(2)

  if x < mask.shape[0] and y < mask.shape[1]:
      if mask[x, y] == 0:  # zero pixel, perform calculation
          min_distance = float('inf')
          sign = 0

          for i in range(reference.shape[0]):
              for j in range(reference.shape[1]):
                  if reference[i, j] == 1:
                      dx = x - i
                      dy = y - j
                      distance = math.sqrt(dx*dx + dy*dy)

                      if distance < min_distance:
                          min_distance = distance
                          sign = -1 if mask[x, y] == reference[i, j] else 1

          output[x, y] = sign * min_distance
      else:
          output[x, y] = 1  # one pixel, excluded from calculation

def cuda_signed_distance_function(mask: np.ndarray, reference: np.ndarray, threads_per_block:Tuple[int,int]=(16, 16)) -> np.ndarray:
  """
  CUDA wrapper function for calculating the signed distance field.
  This function assigns the grid size, moves the data to the GPU, and launches the kernel.

  Args:
    mask (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
    reference (np.ndarray): A 2D array representing the reference points to calculate the distance from.
    threads_per_block (Tuple[int, int]): A tuple representing the number of threads per block in the grid.

  Returns:
    result (np.array): 
    A 2D array representing the signed distance field.
  """
  # Set up CUDA grid
  blocks_per_grid_x = (mask.shape[0] + threads_per_block[0] - 1) // threads_per_block[0]
  blocks_per_grid_y = (mask.shape[1] + threads_per_block[1] - 1) // threads_per_block[1]
  blocks_per_grid = (blocks_per_grid_x, blocks_per_grid_y)

  # Allocate memory on device and copy data
  d_mask = cuda.to_device(mask)
  d_reference = cuda.to_device(reference)
  d_output = cuda.to_device(np.zeros_like(mask, dtype=np.float32))

  # Launch kernel
  cuda_signed_distance_function_kernel[blocks_per_grid, threads_per_block](d_mask, d_reference, d_output)

  # Copy result back to host and return
  return d_output.copy_to_host()


### cpu kernel ###

@njit(parallel=True)
def cpu_signed_distance_function(mask: np.ndarray, reference: np.ndarray) -> np.ndarray:
  """
  CPU function for calculating the signed distance field.
  This function is executed on the CPU in parallel.

  Args:
    mask (np.ndarray): A 2D array representing the input mask as np array where with obstacles 1 and free space as 0.
    reference (np.ndarray): A 2D array representing the reference points to calculate the distance from.

  Returns:
    result (np.ndarray): A 2D array representing the signed distance field.
  """
  output = np.zeros_like(mask, dtype=np.float32)

  for x in prange(mask.shape[0]):
      for y in prange(mask.shape[1]):
          if mask[x, y] == 0:  # zero pixel, perform calculation
              min_distance = float('inf')
              sign = 0

              for i in range(reference.shape[0]):
                  for j in range(reference.shape[1]):
                      if reference[i, j] == 1:
                          dx = x - i
                          dy = y - j
                          distance = math.sqrt(dx*dx + dy*dy)

                          if distance < min_distance:
                              min_distance = distance
                              sign = -1 if mask[x, y] == reference[i, j] else 1

              output[x, y] = sign * min_distance
          else:
              output[x, y] = 1  # one pixel, excluded from calculation

  return output


