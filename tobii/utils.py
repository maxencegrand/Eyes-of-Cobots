import time
from math import sqrt

def timestamp():
    return int(round(time.time() * 1000))

def sleep():
    time.sleep(2)

def sqr(x):
    return x * x

def distance(p1,p2):
    return sqrt(sqr(p2[1]-p1[1])+sqr(p2[0]-p1[0]))
