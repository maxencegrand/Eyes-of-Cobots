import pandas as pd
import csv
import math
import argparse# Create the parser
from pathlib import Path

def get_coord(str):
    return [float(x) for x in str.strip("(')").split(", ")]

def transpose(user, figure):
    DATAPATH = "Documents/Eyes-of-Cobots/eye_trackers_comp/data/recordings"
    PATH = ("%s/%s" % (str(Path.home()), DATAPATH))

    # Open Tobii data csv
    data = "%s/%s/%s/instructions.csv" % \
            (PATH, user, figure)

    # Read csv file
    rows = [["timestamp", \
            "left_x",\
            "left_y",\
            "right_x",\
            "right_y",\
            "left_validity",\
            "right_validity"]]
    with open(data, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='\"')
        first = True
        for row in spamreader:
            if first:
                first = False
                continue
            ts = int(row[18])
            c_left = get_coord(row[2])
            val_left = int(row[6])
            c_right = get_coord(row[10])
            val_right = int(row[14])
            rows.append([ts, c_left[0], c_left[1], c_right[0], c_right[1],\
                    val_left, val_right])

    # Write Lifted Tobii data
    data_lifted = "%s/%s/%s/instructions_norm.csv" % \
            (PATH, user, figure)

    with open(data_lifted , 'w',  newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
