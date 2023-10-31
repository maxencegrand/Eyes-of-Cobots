from position import Position
from point import Point
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD
import colors

class Block:
    def __init__(self, color, shape):
        self.color = color
        self.shape = shape

    def is_a_cube(self):
        return is_a_cube(self.shape)

    def __str__(self):
        if self.is_a_cube():
            return f"{colors.get_name(self.color)} cube"
        else:
            return f"{colors.get_name(self.color)} brick"

    def center(self):
        return self.position.center()

def is_a_cube(shape):
    return shape == get_cube_shape()

def get_cube_shape():
    return 0

def get_brick_shape():
    return 1
