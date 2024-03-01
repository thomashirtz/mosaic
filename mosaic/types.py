from typing import NamedTuple


class Rectangle(NamedTuple):
    y_start: int
    y_end: int
    x_start: int
    x_end: int


class Interval(NamedTuple):
    start: int
    end: int
