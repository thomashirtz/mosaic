from typing import List

import matplotlib.pyplot as plt
import numpy as np
import numpy.typing as npt

from mosaic.types import Rectangle


def plot_image_decomposition(binary_image: npt.NDArray[np.bool_], rectangles: List[Rectangle]) -> None:
    """
    Plot the decomposition of a binary image into rectangles.

    Args:
        binary_image (np.ndarray[np.bool_]): Binary image to be decomposed.
        rectangles (List[Rectangle]): List of rectangles representing the decomposition.
    """

    # Create an RGB image from the binary image for coloring
    blocks_image = np.stack([binary_image] * 3, axis=-1)

    # Define a list of colors for the blocks
    colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
    ]

    color_index = 0
    for rectangle in rectangles:
        for y in range(rectangle.y_start, rectangle.y_end + 1):
            for x in range(rectangle.x_start, rectangle.x_end + 1):
                blocks_image[y, x] = colors[color_index % len(colors)]
        color_index += 1  # Change color for the next block

    # Plotting
    fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(10, 5))
    ax[0].imshow(binary_image, cmap="gray")
    ax[0].set_title("Original Image")
    ax[0].axis("off")

    ax[1].imshow(blocks_image)
    ax[1].set_title("Decomposed Image")
    ax[1].axis("off")

    plt.show()
