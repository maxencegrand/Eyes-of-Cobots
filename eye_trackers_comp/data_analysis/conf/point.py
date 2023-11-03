import numpy as np

class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __str__(self):
        return "(%f, %f)" % (self.x, self.y)

    def distance(other):
        np.linalg.norm(np.array((self.x, self.y)) - np.array((other.x, other.y)))

    def get_vector(self):
        return np.array([self.x,self.y])

def centroid(points):
    n = len(points)
    x = 0
    y = 0
    for point in points:
        x += point.x
        y += point.y
    centroid = Point(float(x/n), float(y/n))
    return centroid

def vectorize(points):
    vector = []
    for p in points:
        vector.append(p.get_vector())
    return np.array(vector)
