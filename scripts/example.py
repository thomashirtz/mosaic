import cv2
import numpy as np

from mosaic import rectangular_decomposition
from mosaic.utilities import plot_image_decomposition

if __name__ == "__main__":
    image_path = "./binary_image.png"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    binary_image = np.logical_not(image.astype(bool)).astype(int)

    rectangles = rectangular_decomposition(binary_image)
    plot_image_decomposition(binary_image, rectangles=rectangles)
