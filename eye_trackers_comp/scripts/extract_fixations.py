import pandas as pd
import csv
import math
from conf.point import Point
from conf.gazepoint import Gazepoint
from conf.fixation import write_csv, create_fixations

CSVFILE = {
"Table" : "table_norm.csv",
"Screen" : "instructions_norm.csv"
}

def is_valid_coord(coord):
    for x in coord:
        if(math.isnan(x)):
            return False
    return True

def is_null_coord(coord):
    for x in coord:
        if(x != 0):
            return False
    return True

def get_coord(c_left, c_right):
    if(is_valid_coord(c_left) and is_valid_coord(c_right)):
        return [float(c_left[0]+c_right[0])/2, float(c_left[1]+c_right[1])/2]
    elif(is_valid_coord(c_left)):
        return c_left
    elif(is_valid_coord(c_right)):
        return c_right
    return c_left

def get_gazepoints(df, steps_duration):
    gazepoints = {}
    # Timestamp -> (Float x Float)
    for idx in range( len(df.index)):
        ts = df.at[idx, "timestamp"]

        if(math.isnan(ts)):
            continue

        c_left = [df.at[idx, "left_x"], df.at[idx, "left_y"]]
        c_right = [df.at[idx, "right_x"], df.at[idx, "right_y"]]
        point = get_coord(c_left, c_right)
        if(is_valid_coord(point)):
            gazepoints[ts] = point

    # Timestamp -> (Float x Float)
    tmp = {}
    idx_ts = 0
    timestamps = list(gazepoints.keys())
    for idx_steps in steps_duration.index:
        begin_ts = steps_duration.at[idx_steps,"timestamp"]
        end_ts = steps_duration.at[idx_steps,"duration"] + begin_ts

        step_id = steps_duration.at[idx_steps,"stepId"]

        while(idx_ts < len(timestamps) and  timestamps[idx_ts] < begin_ts):
            idx_ts += 1
        while(idx_ts < len(timestamps) and  timestamps[idx_ts] < end_ts):
            tmp[timestamps[idx_ts]] = gazepoints[timestamps[idx_ts]]
            idx_ts += 1
    gazepoints = tmp
    return gazepoints

def extract(id, figure, steps_duration):
    csvfile = ("../data/recordings/%s/%s/%s" % (id,figure,CSVFILE["Screen"]))
    df_screen = pd.DataFrame(data=pd.read_csv (csvfile))
    csvfile = ("../data/recordings/%s/%s/%s" % (id,figure,CSVFILE["Table"]))
    df_table = pd.DataFrame(data=pd.read_csv (csvfile))

    gazepoints_screen = create_fixations(get_gazepoints(df_screen, steps_duration))
    gazepoints_table = create_fixations(get_gazepoints(df_table, steps_duration))

    # Merge screen and table
    # Timestamp -> Display x (Float x Float)
    gazepoints = {}
    tmp = {}
    for ts in gazepoints_screen.keys():
        pnt = gazepoints_screen[ts]
        point = Point(pnt[0], pnt[1])
        display = 0
        tmp[ts] = Gazepoint(point, display, ts)
    for ts in gazepoints_table.keys():
        pnt = gazepoints_table[ts]
        point = Point(pnt[0], pnt[1])
        display = 0
        tmp[ts] = Gazepoint(point, display, ts)
    gazepoints = dict(sorted(tmp.items()))

    # Gazepoints
    csvfile = ("../data/%s/fixations_%s.csv" % (id,figure))
    write_csv(csvfile, gazepoints)
