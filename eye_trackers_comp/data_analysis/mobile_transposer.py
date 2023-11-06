import numpy as np
import json
import pandas as pd
import csv, sys
from conf.displays import get_surface, get_display
from conf.point import Point

PATH = "../data/recordings"
PATH_EXPORT = "exports/000/surfaces"
PATH_TO_SAVE = "../data"

KEY_SYNC = "start_time_synced_s"
KEY_SYSTEM = "start_time_system_s"

CSVFILE = {
0 : "instructions2.csv",\
1 : "table2.csv"
}

DISPLAY = {
    0:"Screen",\
    1:"Table",\
    -1:"No Data"
}

SURFACES = {
    "Screen" : [3],\
    "Table" : [0,1,2]
}

def get_offset(user, figure):
    jsonfile = ("%s/%s/%s/info.player.json" % (PATH, user, figure))
    data = json.load(open(jsonfile))
    start_sync = data[KEY_SYNC]
    start_system = data[KEY_SYSTEM]
    return start_system - start_sync

def get_timestamps(user, figure):
    offset = get_offset(user, figure)
    npyfile = ("%s/%s/%s/world_timestamps.npy" % (PATH, user, figure))
    data = np.load(npyfile)
    timestamps = []
    for d in data:
        timestamps.append((d+offset)*1000)
    return timestamps

def transpose_display(user, figure, display, surfaces, timestamps):
    print(get_display(display))
    df_surfaces = {}
    for s in surfaces:
        csvfile = "%s/%s/%s/%s/gaze_positions_on_surface_%s.csv" \
                % (PATH, user, figure, PATH_EXPORT, get_surface(s).get_name())
        df_surfaces[s] = pd.DataFrame(data=pd.read_csv (csvfile))
    rows = [["timestamp", \
            "left_x",\
            "left_y",\
            "right_x",\
            "right_y",\
            "left_validity",\
            "right_validity"]]
    for idx in range(len(timestamps)):
        ts = int(timestamps[idx])
        no_data = True
        for s in surfaces:
            df = df_surfaces[s]
            data = df.loc[df["world_index"] == idx]
            # print(data)

            if(len(data) > 0):
                i = data.index[0]
                if(data.at[i,"on_surf"]):
                    no_data = False
                    left = Point(data.at[i, "x_norm"],data.at[i, "y_norm"])
                    left = get_surface(s).get_absolute_coordinates(left)
                    left = get_surface(s).get_display_coordinates(left)
                    left = get_display(display).get_normalized_coordinates(left)
                    left_conf = data.at[i, "confidence"]
                    rows.append([\
                        ts,\
                        left.x, left.y, left.x, left.y,\
                        left_conf, left_conf])
                    break
                    # sys.exit(1)
        if(no_data):
            rows.append([ts, float("nan"), float("nan"),float("nan"),float("nan"),0,0])

    csvfile = "%s/%s/%s/%s" % \
            (PATH_TO_SAVE, user, figure, CSVFILE[display])
    print(csvfile)
    with open(csvfile , 'w',  newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

def transpose(user, figure):
    timestamps = get_timestamps(user, figure)
    transpose_display(user, figure, 0, SURFACES["Screen"], timestamps)
    transpose_display(user, figure, 1, SURFACES["Table"], timestamps)
    return
