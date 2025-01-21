# **Floor Plan Analytics Package**

Tested Python versions are 3.9 and 3.10

Left to do for publishing alpha version:
- ~~Publish on TestPyPI~~
- ~~Publish on PyPI~~
- ~~Update Test notebooks on Github to using official PyPI~~
- Make public on Github

## **Description**

This is package that includes some of the most used Space Syntax tools to be applied on floor plans or floor plates.
The package is build to utilize Numba to accelerate calculations of the analytics either by CPU multithreading or by utilizing JIT compiled CUDA kernels.

The numba kernels are exclusively written for CUDA, therefore a Nvidia GPU and cuda installation are needed for running the GPU acclerated version of the code.


## **Details**

The inputs and outputs of the outputs fo the methods are all handling Numpy arrays.
This choice is due to two main considerations  aimed to make the backend functions as broadly applicable as possible. 

1. The Input can therefore stem from a (flat and regular) point grid or directly from an image.
2. The output can be used for further data driven analytics, comparing or storage without additional 

To maintain close-to-realtime performance also at larger array sizes, the exposed methods for the analytics calculations include downscale and up sample functionality. 



## **Example Outputs**

Some results of basic usage of the tools:
(more can be found in the '/images' folder)

![Visible Area Image](./images/VisibleArea.png "Visible Area")
![Geodesic Range Image](./images/GeodesicRange.png "Geodesic Range")
![Visible Obstacle Image](./images/VisibleObstacle.png "Visible Obstacle")