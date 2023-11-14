from conf.point import centroid, Point

def min(list):
    m = list[0]
    for item in list:
        if(item < m):
            m = item
    return m

class Position:
    def __init__(self, top_left, top_right, bottom_left, bottom_right):
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

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

    def is_inside(self, point):
        if(point.x < self.top_left.x or point.x < self.bottom_left.x):
            return False
        if(point.x > self.top_right.x or point.x > self.bottom_right.x):
            return False
        if(point.y > self.bottom_right.y or point.y > self.bottom_left.y):
            return False
        if(point.y < self.top_right.y or point.y < self.top_left.y):
            return False
        return True

    def minimal_distance(self,point):
        # print(point)
        #Corner dustance
        distances = [\
            self.top_left.distance(point),\
            self.top_right.distance(point),\
            self.bottom_left.distance(point),\
            self.bottom_right.distance(point)
        ]
        #Plane distance
        if(point.x >= self.top_left.x and point.x <= self.top_right.x):
            distances.append(Point(point.x,self.top_left.y).distance(point))
            distances.append(Point(point.x,self.top_right.y).distance(point))
        if(point.x >= self.bottom_left.x and point.x <= self.bottom_right.x):
            distances.append(Point(point.x,self.bottom_left.y).distance(point))
            distances.append(Point(point.x,self.bottom_right.y).distance(point))
        if(point.y >= self.bottom_right.x and point.x <= self.top_right.x):
            distances.append(Point(self.bottom_right.x,point.y).distance(point))
            distances.append(Point(self.top_right.x,point.y).distance(point))
        if(point.y >= self.bottom_left.x and point.x <= self.top_left.x):
            distances.append(Point(self.bottom_left.x,point.y).distance(point))
            distances.append(Point(self.top_left.x,point.y).distance(point))

        if(self.is_inside(point)):
            return 0-min(distances)
        return min(distances)

    def __str__(self):
        str = "["
        str += f"{self.top_left},"
        str += f"{self.top_right},"
        str += f"{self.bottom_right},"
        str += f"{self.bottom_left}"
        return str

def is_horizontal(horizontal):
    return horizontal == get_horizontal()

def get_horizontal():
    return 1

def get_vertical():
    return 0

def create_position_from_size(top_left, width, height):
    top_left = top_left
    top_right = Point(top_left.x+width, top_left.y)
    bottom_left = Point(top_left.x, top_left.y+height)
    bottom_right = Point(top_left.x+width, top_left.y+height)
    return Position(top_left, top_right, bottom_left, bottom_right)

def create_position(block, top_left, horizontal):
    # The block is a cube
    if(block.is_a_cube()):
        return Position(\
            Point(top_left.x,top_left.y),\
            Point(top_left.x+1,top_left.y),\
            Point(top_left.x,top_left.y+1),\
            Point(top_left.x+1,top_left.y+1))
    else:
        if(is_horizontal(horizontal)):
            return Position(\
                Point(top_left.x,top_left.y),\
                Point(top_left.x+3,top_left.y),\
                Point(top_left.x,top_left.y+1),\
                Point(top_left.x+3,top_left.y+1))
        else:
            return Position(\
                Point(top_left.x,top_left.y),\
                Point(top_left.x+1,top_left.y),\
                Point(top_left.x,top_left.y+3),\
                Point(top_left.x+1,top_left.y+3))
