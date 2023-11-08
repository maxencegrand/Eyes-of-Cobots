import pandas as pd
import csv
import math
from conf.displays import ID_SCREEN, ID_TABLE

DISPLAY = {
    ID_SCREEN:"Screen",\
    ID_TABLE:"Table",\
    -1:"No Data"
}

CSVFILE = {
"Table" : "table2.csv",
"Screen" : "instructions2.csv"
}

def get_coord(str):
    return [float(x) for x in str.strip("(')").split(", ")]

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

# is_on_display Timestamp -> Bool
# Return Step -> (Timsestamp -> (Display x Duration))
def get_display_interval(is_on_display, display_id, steps_durations):
    # Step -> (Timestampe -> Display)
    tmp = {}
    idx_ts = 0
    timestamps = list(is_on_display.keys())
    for idx_steps in range(len(steps_durations)):
        # begin and end timestamp of the step
        begin_ts = steps_durations[idx_steps].begin
        end_ts = steps_durations[idx_steps].end
        step_id = steps_durations[idx_steps].id

        tmp[step_id] = {}

        while(idx_ts < len(timestamps) and  timestamps[idx_ts] < begin_ts):
            idx_ts += 1
        while(idx_ts < len(timestamps) and  timestamps[idx_ts] < end_ts):
            tmp[step_id][timestamps[idx_ts]] = display_id if \
                        is_on_display[timestamps[idx_ts]] else -1
            idx_ts += 1
    is_on_display = tmp

    # Compress screen info
    tmp = {}
    steps = list(is_on_display.keys())
    idx_ts = 0
    current_step = steps[idx_ts]
    current_begin = is_on_display
    for current_step in steps:
        tmp[current_step] = {}
        timestamps = list(is_on_display[current_step].keys())
        idx_ts = 0
        current_begin = timestamps[idx_ts]
        current_d = is_on_display[current_step][current_begin]
        current_end = current_begin
        for idx_ts in range(len(timestamps)):
            ts = timestamps[idx_ts]
            current_end = ts
            d = is_on_display[current_step][ts]
            if(current_d == d):
                continue
            else:
                duration = current_end-current_begin
                if(duration > 0):
                    if(current_d != -1):
                        tmp[current_step][current_begin] = [current_d, duration]
                    current_begin = ts
                    current_end = ts
                    current_d = d
        duration = current_end-current_begin
        if(duration > 0):
            if(current_d != -1):
                tmp[current_step][current_begin] = [current_d, duration]
    is_on_display = tmp
    return is_on_display

# df : Gazepoint DataFrame
# display id : id of the display (0, 1)
# steps_durations : steps DataFrame with durations
# Return Step -> (Timsestamp -> (Display x Duration))
def get_data_display(df, display_id, steps_durations):
    # Is_on ID -> (Timsestamp -> Bool)
    is_on = {}
    for idx in range( len(df.index)):
        ts = df.at[idx, "timestamp"]

        if(math.isnan(ts)):
            continue

        c_left = [df.at[idx, "left_x"], df.at[idx, "left_y"]]
        c_right = [df.at[idx, "right_x"], df.at[idx, "right_y"]]

        if(is_valid_coord(c_left) or is_valid_coord(c_right)):
            is_on[ts]=True
        else:
            is_on[ts]=False

    is_on = get_display_interval(is_on, display_id, steps_durations)
    return is_on

def extract(id, figure, steps_durations):
    csvfile = ("../data/%s/%s/%s" % (id,figure,CSVFILE["Screen"]))
    df_screen = pd.DataFrame(data=pd.read_csv (csvfile))
    idx_screen = 0
    csvfile = ("../data/%s/%s/%s" % (id,figure,CSVFILE["Table"]))
    df_table = pd.DataFrame(data=pd.read_csv (csvfile))
    idx_table = 0

    is_on_screen = get_data_display(df_screen, ID_SCREEN, steps_durations)
    is_on_table = get_data_display(df_table, ID_TABLE, steps_durations)

    # Merge screen and table
    is_on_display = {}
    for step in list(is_on_screen.keys()):
        is_on_display[step] = \
                dict(sorted({**is_on_screen[step], **is_on_table[step]}.items()))

    # Display durations
    csvfile = ("../data/%s/%s/displays.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["stepId", "timestamp", "displayId", "duration"])
        for step in list(is_on_display.keys()):
            for ts in list(is_on_display[step].keys()):
                spamwriter.writerow([step, ts, \
                        is_on_display[step][ts][0],\
                        is_on_display[step][ts][1]])
