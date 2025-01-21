import numpy as np
import numba as nb

from PIL import Image
import PIL.Image

from scipy.ndimage import zoom



def resize_image(img: PIL.Image, size: int) -> PIL.Image:
    """
    Resize an image according to the smaller dimension.
    
    Args:
        img (PIL.Image): Image to be resized.
        size (int): Size of the smaller dimension.
        
    Returns:
        img (PIL.Image): Resized
    """
    h, w = img.size
    if h < w:
        new_h = size
        new_w = int(w * size / h)
    else:
        new_h = int(h * size / w)
        new_w = size

    img = img.resize((new_h, new_w), Image.LANCZOS)
    return img


def resize_array(array: np.ndarray, new_size: int, rescale_by_larger: bool = True) -> np.ndarray:
    """
    Resize a 2D NumPy array to a new size specified by a single dimension.
    
    Args:
        array (np.ndarray): 2D NumPy array to resize.
        new_size (int): New size of the array.
        
    Returns:
        array (np.ndarray): Resized 2D NumPy array.
    """
    height, width = array.shape
    aspect_ratio = width / height

    if rescale_by_larger:
        if width >= height:
            new_width = new_size
            new_height = int(new_size / aspect_ratio)
        else:
            new_height = new_size
            new_width = int(new_size * aspect_ratio)
    else:
        if width >= height:
            new_height = new_size
            new_width = int(new_size * aspect_ratio)
        else:
            new_width = new_size
            new_height = int(new_size / aspect_ratio)


    zoom_factors = (new_height / height, new_width / width)
    return zoom(array, zoom_factors, order=1)


def resize_array_xy(array: np.ndarray, new_size: np.ndarray) -> np.ndarray:
    """
    Resize a 2D NumPy array to a new size specified by x and y dimensions.

    Args:
        array (np.ndarray): 2D NumPy array to resize
        new_size (np.ndarray): New size of the array
        
    Returns:
        array (np.ndarray): Resized 2D NumPy array.
    """
    height, width = array.shape
    new_height, new_width = new_size

    zoom_factors = (new_height / height, new_width / width)
    return zoom(array, zoom_factors, order=1)


def convert_2d_to_3d(image_2d: np.ndarray) -> np.ndarray:
    """
    Convert a 2D image to a 3D image by repeating the 2D image along a new axis.
    
    Args:
        image_2d (np.ndarray): 2D NumPy array representing the image.
    
    Returns:
        image_3d (np.ndarray): 3D NumPy array representing the image.
    """
    # Ensure the input is a 2D numpy array
    if len(image_2d.shape) != 2:
        raise ValueError("Input must be a 2D numpy array")

    # Create a 3D array by repeating the 2D array along a new axis
    image_3d = np.repeat(image_2d[:, :, np.newaxis], 3, axis=2)

    return image_3d


def convert_3d_to_2d(image_3d: np.ndarray) -> np.ndarray:
    """
    CUDA kernel for flood fill algorithm.
    This function is executed on the GPU.

    Parameters:
        image_3d (np.ndarray): 3D NumPy array representing the image.

    Returns:
        changes (np.ndarray): 2D NumPy array representing the image.
    """
    image_3d = np.array(image_3d)

    # Check if the input is 3D
    if len(image_3d.shape) != 3:
        raise ValueError("Input must be a 3D image array")

    # Calculate the mean across the depth dimension
    avg_values = np.mean(image_3d, axis=2)
    # Normalize the values to [0, 1] range
    normalized_values = (avg_values - np.min(avg_values)) / (np.max(avg_values) - np.min(avg_values))
    # Round the values to either 0 or 1
    image_2d = np.round(normalized_values).astype(int)

    return image_2d


def scale_coordinates(coordinates: np.ndarray, original_size: np.ndarray, new_size: np.ndarray) -> np.ndarray:  
    """
    Scale coordinates from the original size to the new size.

    Parameters:
        coordinates (np.ndarray): 1D NumPy array representing the coordinates to be scaled.
        original_size (np.ndarray): 1D NumPy array representing the original size.
        new_size (np.ndarray): 1D NumPy array representing the new size.
        
    Returns:
        scaled_coordinates (np.ndarray): 1D NumPy array representing the scaled coordinates.
    """
    return [int(coordinate * new_size / original_size) for coordinate in coordinates]
