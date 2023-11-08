import conf.gazepoint as gz
from conf.step import get_step
from conf.displays import get_display
import csv
import os

KEY_ID = "id"
KEY_ACTION = "actionId"
KEY_COLOR = "colorId"
KEY_SHAPE = "shapeId"
KEY_X1 = "x1"
KEY_Y1 = "y1"
KEY_X2 = "x2"
KEY_Y2 = "y2"
KEY_X3 = "x3"
KEY_Y3 = "y3"
KEY_X4 = "x4"
KEY_Y4 = "y4"

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
    event_dir = "../data/%s/%s/events" % (id,figure)

    if(not os.path.exists(event_dir)):
        os.mkdir("../data/%s/%s/events" % (id,figure))
    csv_label = ("%s/labels.csv" % event_dir)
    with open(csv_label, 'w', newline='') as csv_label:
        spamwriter = csv.writer(csv_label, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_ID, KEY_ACTION, KEY_COLOR, KEY_SHAPE,\
            KEY_X1, KEY_Y1, KEY_X2, KEY_Y2, KEY_X3, KEY_Y3, KEY_X4, KEY_Y4])
        id_event = 0
        for event in events:
            spamwriter.writerow(event.get_rows(id_event))
            csv_dist = ("%s/%d_table.csv" % (event_dir, id_event))
            with open(csv_dist, 'w', newline='') as csv_dist:
                spamwriter_dist = csv.writer(csv_dist, delimiter=',',\
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                spamwriter_dist.writerow(["timestamp", "distance"])
                ts = event.timestamp
                step = get_step(ts, steps)
                if(previous == -1):
                    previous = step.begin
                points = get_points(previous, ts, gazepoints_table)

                first_ts = list(points.keys())[0]
                for ts in points.keys():
                    dist = event.minimal_distance(points[ts].point)
                    spamwriter_dist.writerow([(ts-first_ts), dist])
                previous = ts
            id_event += 1

    return
