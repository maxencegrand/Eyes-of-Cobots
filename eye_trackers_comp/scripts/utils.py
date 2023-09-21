import numpy as np

def centroid(coordinates):
    arr = np.asarray(coordinates)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return [sum_x/length, sum_y/length]

def _sum(list):
    s = 0
    for x in list:
        s += x
    return s

def distance(p1, p2):
     return np.linalg.norm(np.asarray(p1)-np.asarray(p2))

def min(list):
    m = list[0]
    for item in list:
        if(item < m):
            m = item
    return m

def distance_min_block_corner(position, block_positions):
    dist = [distance(position, p) for p in block_positions]
    dist.append(distance(position, centroid(block_positions)))
    return min(dist)
