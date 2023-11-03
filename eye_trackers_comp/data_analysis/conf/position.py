from conf.point import centroid, Point

def min(list):
    m = list[0]
    for item in list:
        if(item < m):
            m = item
    return m

class Position:
    def __init__(self, surface, top_left, top_right, bottom_left, bottom_right):
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left
        self.surface = surface

    def center(self):
        return centroid([self.top_left, self.top_right,\
                            self.bottom_right, self.bottom_left])

    def distance_from_center(self, point):
        return self.center().distance(point)

    def get_all_points(self):
        return [\
            self.top_left,\
            self.top_right,\
            self.bottom_right,\
            self.bottom_left]

    def minimal_distance(self,point):
        distances = [\
            self.top_left.distance(point),\
            self.top_right.distance(point),\
            self.bottom_left.distance(point),\
            self.bottom_right.distance(point)
        ]
        return min(distances)

    def __str__(self):
        str = "["
        str += f"{self.top_left},"
        str += f"{self.top_right},"
        str += f"{self.bottom_right},"
        str += f"{self.bottom_left}"
        str += f"] in {self.surface}"
        return str

def is_horizontal(horizontal):
    return horizontal == get_horizontal()

def get_horizontal():
    return 1

def get_vertical():
    return 0

def create_position(block, top_left, horizontal, surface):
    # The block is a cube
    if(block.is_a_cube()):
        return Position(surface,\
            Point(top_left.x,top_left.y),\
            Point(top_left.x+1,top_left.y),\
            Point(top_left.x,top_left.y+1),\
            Point(top_left.x+1,top_left.y+1))
    else:
        if(is_horizontal(horizontal)):
            return Position(surface,\
                Point(top_left.x,top_left.y),\
                Point(top_left.x+3,top_left.y),\
                Point(top_left.x,top_left.y+1),\
                Point(top_left.x+3,top_left.y+1))
        else:
            return Position(surface, \
                Point(top_left.x,top_left.y),\
                Point(top_left.x+1,top_left.y),\
                Point(top_left.x,top_left.y+3),\
                Point(top_left.x+1,top_left.y+3))
