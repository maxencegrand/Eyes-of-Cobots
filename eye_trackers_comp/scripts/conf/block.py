from position import Position
from point import Point
from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD
import colors

class Block:
    def __init__(self, color, shape, top_left, horizontal, surface):
        self.color = color
        self.shape = shape
        self.surface = surface

        # The block is a cube
        if(is_a_cube(shape)):
            self.position = Position(\
                Point(top_left[0],top_left[1]),\
                Point(top_left[0]+1,top_left[1]),\
                Point(top_left[0],top_left[1]+1),\
                Point(top_left[0]+1,top_left[1]+1))
        else:
            if(is_horizontal(horizontal)):
                self.position = Position(\
                    Point(top_left[0],top_left[1]),\
                    Point(top_left[0]+3,top_left[1]),\
                    Point(top_left[0],top_left[1]+1),\
                    Point(top_left[0]+3,top_left[1]+1))
            else:
                self.position = Position(\
                    Point(top_left[0],top_left[1]),\
                    Point(top_left[0]+1,top_left[1]),\
                    Point(top_left[0],top_left[1]+3),\
                    Point(top_left[0]+1,top_left[1]+3))

        def is_a_cube(self):
            return is_a_cube(self.shape)

        def __str__(self):
            if self.is_a_cube():
                return f"{colors.get_name(self.color)} cube at {self.center()}"
            else
                return f"{colors.get_name(self.color)} brick at {self.center()}"

    def center(self):
        return self.position.center()

def is_a_cube(shape):
    return shape == get_cube_shape()

def get_cube_shape():
    return 0

def get_brick_shape():
    return 1

def is_horizontal(horizontal):
    return horizontal == get_horizontal()

def get_horizontal():
    return 1

def get_vertical():
    return 0
