import conf.gazepoint as gz
from conf.step import get_step
from conf.displays import get_display
from conf.actions import get_name
from conf.stock import Stock
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

def extract_pick(event_dir, steps, events, gazepoints_table):
    stock = Stock()
    previous = -1
    csv_label = ("%s/pick/labels.csv" % event_dir)
    with open(csv_label, 'w', newline='') as csv_label:
        spamwriter = csv.writer(csv_label, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_ID, KEY_COLOR, KEY_SHAPE,\
            KEY_X1, KEY_Y1, KEY_X2, KEY_Y2, KEY_X3, KEY_Y3, KEY_X4, KEY_Y4])
        id_event = 0
        for event in events:
            if(not event.isPick()):
                continue
            spamwriter.writerow(event.get_rows(id_event))
            csv_dist = ("%s/pick/%d_table.csv" % (event_dir, id_event))
            with open(csv_dist, 'w', newline='') as csv_dist:
                spamwriter_dist = csv.writer(csv_dist, delimiter=',',\
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                spamwriter_dist.writerow(["timestamp", "block_to_pick", "stock_to_pick","color_to_pick", "shape_to_pick"])
                ts = event.timestamp
                step = get_step(ts, steps)
                if(previous == -1):
                    previous = step.begin
                points = get_points(previous, ts, gazepoints_table)

                first_ts = list(points.keys())[0]
                # print(event.block)
                position_stock = stock.get_position_stock(\
                                                        event.block.id,\
                                                        event.block.shape,\
                                                        event.block.color)
                position_stock = get_display(1).get_real_position_from_absolute(\
                                                    position_stock)
                position_shape = stock.get_position_shape(\
                                                        event.block.id,\
                                                        event.block.shape,\
                                                        event.block.color)
                position_shape = get_display(1).get_real_position_from_absolute(\
                                                    position_shape)
                position_color = stock.get_position_color(\
                                                        event.block.id,\
                                                        event.block.shape,\
                                                        event.block.color)
                position_color = get_display(1).get_real_position_from_absolute(position_color)
                for ts in points.keys():
                    dist_block = event.minimal_distance(points[ts].point)
                    dist_stock = position_stock.minimal_distance(points[ts].point)
                    dist_shape = position_shape.minimal_distance(points[ts].point)
                    dist_color = position_color.minimal_distance(points[ts].point)
                    spamwriter_dist.writerow([(ts-first_ts), dist_block,dist_stock,dist_shape,dist_color])
                previous = ts
            id_event += 1

def extract_place(event_dir, steps, events, gazepoints_table):
    stock = Stock()
    previous = -1
    csv_label = ("%s/place/labels.csv" % event_dir)
    with open(csv_label, 'w', newline='') as csv_label:
        spamwriter = csv.writer(csv_label, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_ID, KEY_COLOR, KEY_SHAPE,\
            KEY_X1, KEY_Y1, KEY_X2, KEY_Y2, KEY_X3, KEY_Y3, KEY_X4, KEY_Y4])
        id_event = 0
        for event in events:
            if(not event.isPlace()):
                continue
            spamwriter.writerow(event.get_rows(id_event))
            csv_dist = ("%s/place/%d_table.csv" % (event_dir, id_event))
            with open(csv_dist, 'w', newline='') as csv_dist:
                spamwriter_dist = csv.writer(csv_dist, delimiter=',',\
                                    quotechar='\"', quoting=csv.QUOTE_MINIMAL)
                spamwriter_dist.writerow(["timestamp", "pos_to_place", "expand_1","expand_2", "expand_4"])
                ts = event.timestamp
                step = get_step(ts, steps)
                if(previous == -1):
                    previous = step.begin
                points = get_points(previous, ts, gazepoints_table)

                first_ts = list(points.keys())[0]
                pos = event.position
                pos = get_display(1).get_normalized_position_from_real(pos)
                pos = get_display(1).get_absolute_position(pos)
                expand_1 = get_display(1).get_real_position_from_absolute(\
                                                                pos.expand(1,1))
                expand_2 = get_display(1).get_real_position_from_absolute(\
                                                                pos.expand(2,2))
                expand_4 = get_display(1).get_real_position_from_absolute(\
                                                                pos.expand(4,4))
                for ts in points.keys():
                    dist_to_place = event.minimal_distance(points[ts].point)
                    dist_to_expand_1 = expand_1.minimal_distance(points[ts].point)
                    dist_to_expand_2 = expand_2.minimal_distance(points[ts].point)
                    dist_to_expand_4 = expand_4.minimal_distance(points[ts].point)
                    spamwriter_dist.writerow([\
                                    (ts-first_ts),\
                                    dist_to_place,\
                                    dist_to_expand_1,\
                                    dist_to_expand_2,\
                                    dist_to_expand_4])
                previous = ts
            id_event += 1

def extract(id, figure, steps, events):
    gazepoints_table = gz.read_csv("../data/%s/%s/gazepoints_table.csv" %\
            (id, figure))

    idx = 0
    event_dir = "../data/%s/%s/events" % (id,figure)

    if(not os.path.exists(event_dir)):
        os.mkdir("../data/%s/%s/events" % (id,figure))
        os.mkdir("../data/%s/%s/events/pick" % (id,figure))
        os.mkdir("../data/%s/%s/events/place" % (id,figure))

    extract_pick(event_dir, steps, events, gazepoints_table)
    extract_place(event_dir, steps, events, gazepoints_table)

    return
