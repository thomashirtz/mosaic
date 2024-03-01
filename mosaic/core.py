from typing import List

import numpy as np

from mosaic.types import Rectangle, Interval


def rectangular_decomposition(image: np.ndarray[np.bool_]) -> List[Rectangle]:
    """
    Performs rectangular decomposition on a single binary image, identifying and grouping contiguous
    foreground regions into rectangular blocks.

    This function iterates through each line of the image, identifying contiguous foreground intervals
    and grouping them into rectangles based on their spatial continuity across lines. Rectangles are
    extended or initiated based on their alignment with intervals in subsequent lines.

    Args:
        image (np.ndarray[np.bool_]): A binary image as a 2D NumPy array where True represents
                                       foreground pixels and False represents background.

    Returns:
        List[Rectangle]: A list of Rectangle namedtuples, each representing a rectangular block
                         identified within the image. Each Rectangle contains start and end coordinates
                         on the y-axis (y_start, y_end) and x-axis (x_start, x_end).
    """

    # Assert that the image is a 2D array
    assert image.ndim == 2, "Input image must be a 2D array"
    height, width = image.shape

    # Initialize a list to store the rectangles found in the image
    rectangles = []

    # Iterate over each line of the image
    for y in range(height):
        line_intervals = []  # List to hold intervals found in the current line
        start = None  # Variable to mark the start of a new interval

        # Scan through pixels in the line
        for x in range(width):
            # If a foreground pixel is found, and we are not currently tracking an interval
            if image[y, x] == 1 and start is None:
                start = x  # Mark this as the start of a new interval
            # If a background pixel is found, and we are currently tracking an interval
            elif image[y, x] == 0 and start is not None:
                # Add the interval to the list and reset start
                line_intervals.append(Interval(start=start, end=x - 1))
                start = None
        # If the line ends while still tracking an interval, close the interval at the end of the line
        if start is not None:
            line_intervals.append(Interval(start=start, end=width - 1))

        # Process the found intervals in relation to previous lines
        for interval in line_intervals:
            matched = False
            for i, rectangle in enumerate(rectangles):
                # Check if the interval matches exactly with the previous rectangle's interval
                if rectangle.y_end == y-1 and interval.start == rectangle.x_start and interval.end == rectangle.x_end:
                    # Extend the rectangle to include the new interval by updating y_end
                    rectangles[i] = Rectangle(
                        y_start=rectangle.y_start,
                        y_end=y,
                        x_start=rectangle.x_start,
                        x_end=rectangle.x_end
                    )
                    matched = True
                    break
            # If the interval does not match any existing rectangle, start a new rectangle
            if not matched:
                rectangle = Rectangle(
                    y_start=y,
                    y_end=y,
                    x_start=interval[0],
                    x_end=interval[1]
                )
                rectangles.append(rectangle)

    return rectangles


def batch_rectangular_decomposition(image_batch: np.ndarray) -> List[List[Rectangle]]:
    """
    Processes a batch of binary images, applying rectangular decomposition to each image in the batch.
    This function is designed to handle multiple images at once, iterating through each image and
    decomposing it into rectangular blocks.

    Args:
        image_batch (np.ndarray): A 3D NumPy array of binary images with shape (B, W, H), where B is
                                  the batch size (number of images), and W and H are the width and height
                                  of each image, respectively.

    Returns:
        List[List[Rectangle]]: A list where each element is a list of Rectangle namedtuples for the
                               corresponding image in the batch. Each Rectangle represents a rectangular
                               block identified in that image.
    """
    # Ensure the input is a 3D array representing a batch of images
    if image_batch.ndim != 3:
        raise ValueError("Input must be a 3D array of shape (B, W, H).")

    results = []
    # Iterate through each image in the batch
    for image in image_batch:
        # Process each image individually and append the result to results
        decomposition = rectangular_decomposition(image)
        results.append(decomposition)

    return results
