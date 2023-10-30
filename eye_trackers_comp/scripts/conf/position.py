from point import centroid

class Position:
    def __init__(self, top_left, top_right, bottom_right, bottom_left):
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.bottom_left = bottom_left

    def center(self):
        return centroid([self.top_left, self.top_right,\
                            self.bottom_right, self.bottom_left])

    def __str__(self):
        return center()
