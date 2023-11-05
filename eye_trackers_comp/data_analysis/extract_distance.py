import conf.gazepoint as gz
from conf.step import get_step
from conf.displays import get_display

def get_points(begin, end, points):
    res = {}
    for ts in points.keys():
        if(ts <= end and ts >= begin):
            res[ts] = points[ts]
    return res

def extract(id, figure, steps, events):
    gazepoints_table = gz.read_csv("../data/%s/%s/gazepoints_table.csv" %\
            (id, figure))
    previous = -1
    idx = 0
    for event in events:
        print(event)
        ts = event.timestamp
        step = get_step(ts, steps)
        print(step)
        if(previous == -1):
            previous = step.begin
        points = get_points(previous, ts, gazepoints_table)
        points_absolute = {}
        for ts in points.keys():
            points_absolute[ts] = gz.Gazepoint(\
                get_display(1).get_real_coordinates(points[ts].point), ts)
            print(f"{points[ts]} -> {points_absolute[ts]}")

        first_ts = list(points.keys())[0]
        distance = {}
        for ts in points_absolute.keys():
            dist = event.minimal_distance(points_absolute[ts].point)
            # dist *= 16
            print(f"{ts-first_ts}: {dist}")
            distance[ts-first_ts] = dist
        previous = ts
        
    return
