import numpy as np
import csv

def centroid(coordinates):
    arr = np.asarray(coordinates)
    length = arr.shape[0]
    sum_x = np.sum(arr[:, 0])
    sum_y = np.sum(arr[:, 1])
    return [sum_x/length, sum_y/length]
