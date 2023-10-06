import pandas as pd
import csv
import sys, getopt
from conf import Users, Figures
from table_loader import _LOAD,_GET_ALL
import math

DISPLAY = {
    0:"Screen",\
    1:"Table",\
    -1:"No_Display"
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

def extract_displays(id, figure, df_actions):
    csvfile = ("../data/recordings/%s/%s/Screen.csv" % (id,figure))
    df_screen = _LOAD(csvfile)
    idx_screen = 0
    csvfile = ("../data/recordings/%s/%s/Table.csv" % (id,figure))
    df_table = _LOAD(csvfile, sep="\t")
    idx_table = 0

    # Add all timestamps
    all_timestamps = []
    for t in df_screen["timestamp"].tolist():
        all_timestamps.append(t)
    for t in df_table["System Time"].tolist():
        all_timestamps.append(int(t/1000))


    all_timestamps = sorted(all_timestamps)
    idx_current_timestamp = 0
    is_on_screen = []
    while idx_screen < len(df_screen.index):
        t_screen = df_screen.at[idx_screen, "timestamp"]
        c_left = get_coord(df_screen.at[idx_screen, \
                        "left_gaze_point_on_display_area"])
        c_right = get_coord(df_screen.at[idx_screen, \
                        "right_gaze_point_on_display_area"])
        if(is_valid_coord(c_left) or is_valid_coord(c_right)):
            is_on_screen.append([t_screen, True])
        else:
            is_on_screen.append([t_screen, False])
        idx_screen += 1
    is_on_table = []
    while idx_table < len(df_table.index):
        t_table = int(df_table.at[idx_table, "System Time"]/1000)
        try:
            c_left = [float(df_table.at[idx_table, "Lft X Pos"]),\
                        float(df_table.at[idx_table, "Lft Y Pos"])]
            c_right = [float(df_table.at[idx_table, "Rt X Pos"]),\
                        float(df_table.at[idx_table, "Rt Y Pos"])]
            if(is_null_coord(c_left) and is_null_coord(c_right)):
                is_on_table.append([t_table, False])
            else:
                is_on_table.append([t_table, True])
        except:
            is_on_table.append([t_table, True])
        idx_table += 1
    idx_screen = 0
    idx_table = 0
    displays = []
    for t in all_timestamps:
        is_on_display = False
        #Check if t is on screen
        if(idx_screen < len(is_on_screen)):
            while(idx_screen < len(is_on_screen) and \
                    t > is_on_screen[idx_screen][0]):
                idx_screen += 1
            if(idx_screen < len(is_on_screen) and\
                    t == is_on_screen[idx_screen][0]):
                if(is_on_screen[idx_screen][1]):
                    is_on_display = True
                    displays.append([t, 0])
        #Check if t is on table
        if(idx_table < len(is_on_table)):
            while(idx_table < len(is_on_table) and\
                    t > is_on_table[idx_table][0]):
                idx_table += 1
            if(idx_table < len(is_on_table) and\
                    t == is_on_table[idx_table][0]):

                if(is_on_table[idx_table][1]):
                    is_on_display = True
                    displays.append([t, 1])
        #Check if t is neither on the screen nor on the table
        if(not is_on_display):
            displays.append([t, -1])
    #Add step infos
    tmp = []
    idx_d = 0
    for idx_action in df_actions.index:
        begin_ts = df_actions.at[idx_action,"begin"]
        end_ts = df_actions.at[idx_action,"end"]
        while(idx_d < len(displays) and displays[idx_d][0] < begin_ts):
            idx_d += 1
        while(idx_d < len(displays) and displays[idx_d][0] < end_ts):
            step_id = df_actions.at[idx_action,"stepId"]
            action_id = df_actions.at[idx_action,"actionId"]
            tmp.append([step_id, action_id, displays[idx_d][0], displays[idx_d][1]])
            idx_d += 1
    displays = tmp
    #Compress displays info
    tmp = []
    idx_d = 0
    current_step = displays[0][0]
    current_action = displays[0][1]
    current_begin = displays[0][2]

    current_d = displays[0][3]
    idx_d = 1
    for idx_d in range(len(displays)):
        step = displays[idx_d][0]
        action = displays[idx_d][1]
        t = displays[idx_d][2]
        current_end = t
        d = displays[idx_d][3]
        if(step == current_step and action == current_action):
            if(current_d == d):
                current_end = t
            else:
                # if(idx_d < len(displays)-1 and
                #     current_d == displays[idx_d+1][3]):
                #     continue
                if(current_end - current_begin > 0):
                    tmp.append([current_step, current_action, current_d,\
                            current_begin, current_end - current_begin])
                current_begin = t
                current_end = t
                current_d = d
        else:
            # if(idx_d < len(displays)-1 and
            #     current_d == displays[idx_d+1][3]):
            #     continue
            if(current_end - current_begin > 0):
                tmp.append([current_step, current_action, current_d,\
                        current_begin, current_end - current_begin])
            current_begin = t
            current_end = t
            current_d = d
            current_step = step
            current_action = action
    displays = tmp
    # Write display csvfile
    csvfile = ("../data/%s_%s_displays.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["stepId", "actionId", "display", "timestamp", "duration"])
        for d in displays:
            spamwriter.writerow(d)

def get_display_interval(is_on_display, display_value, df_actions):
    tmp = []
    idx_d = 0
    for idx_action in df_actions.index:
        begin_ts = df_actions.at[idx_action,"begin"]
        end_ts = df_actions.at[idx_action,"end"]
        while(idx_d < len(is_on_display) and is_on_display[idx_d][0] < begin_ts):
            idx_d += 1
        while(idx_d < len(is_on_display) and is_on_display[idx_d][0] < end_ts):
            step_id = df_actions.at[idx_action,"stepId"]
            action_id = df_actions.at[idx_action,"actionId"]
            tmp.append([step_id, action_id, is_on_display[idx_d][0], \
                    (display_value if is_on_display[idx_d][1] else -1)])
            idx_d += 1
    is_on_display = tmp
    # Compress screen info
    tmp = []
    idx_d = 0
    current_step = is_on_display[0][0]
    current_action = is_on_display[0][1]
    current_begin = is_on_display[0][2]

    current_d = is_on_display[0][3]
    idx_d = 1
    for idx_d in range(len(is_on_display)):
        step = is_on_display[idx_d][0]
        action = is_on_display[idx_d][1]
        t = is_on_display[idx_d][2]
        current_end = t
        d = is_on_display[idx_d][3]
        if(step == current_step and action == current_action):
            if(current_d == d):
                current_end = t
            else:
                # if(idx_d < len(displays)-1 and
                #     current_d == displays[idx_d+1][3]):
                #     continue
                if(current_end - current_begin > 0):
                    tmp.append([current_step, current_action, current_d,\
                            current_begin, current_end - current_begin])
                current_begin = t
                current_end = t
                current_d = d
        else:
            # if(idx_d < len(displays)-1 and
            #     current_d == displays[idx_d+1][3]):
            #     continue
            if(current_end - current_begin > 0):
                tmp.append([current_step, current_action, current_d,\
                        current_begin, current_end - current_begin])
            current_begin = t
            current_end = t
            current_d = d
            current_step = step
            current_action = action
    is_on_display = tmp
    return is_on_display

def check_if_on_display(t, display, display_value):
    for idx in range(len(display)):
        if(t >= display[idx][3] and t <= display[idx][3] + display[idx][4]):
            if(display[idx][2] == display_value):
                return True
    return False
def extract_displays_bis(id, figure, df_actions):
    csvfile = ("../data/recordings/%s/%s/Screen.csv" % (id,figure))
    df_screen = _LOAD(csvfile)
    idx_screen = 0
    csvfile = ("../data/recordings/%s/%s/Table.csv" % (id,figure))
    df_table = _LOAD(csvfile, sep="\t")
    idx_table = 0

    # Add all timestamps
    # all_timestamps = []
    # for t in df_screen["timestamp"].tolist():
    #     all_timestamps.append(t)
    # for t in df_table["System Time"].tolist():
    #     all_timestamps.append(int(t/1000))


    # all_timestamps = sorted(all_timestamps)
    # Screen data
    idx_current_timestamp = 0
    is_on_screen = []
    for idx_screen in range( len(df_screen.index)):
        t_screen = df_screen.at[idx_screen, "timestamp"]
        # try:
        if(math.isnan(t_screen)):
            continue
        c_left = get_coord(df_screen.at[idx_screen, \
                        "left_gaze_point_on_display_area"])
        c_right = get_coord(df_screen.at[idx_screen, \
                        "right_gaze_point_on_display_area"])
        if(is_valid_coord(c_left) or is_valid_coord(c_right)):
            is_on_screen.append([t_screen, True])
        else:
            is_on_screen.append([t_screen, False])
    is_on_screen = get_display_interval(is_on_screen, 0, df_actions)
    print(is_on_screen)

    # Table data
    is_on_table = []
    while idx_table < len(df_table.index):
        t_table = int(df_table.at[idx_table, "System Time"]/1000)
        try:
            c_left = [float(df_table.at[idx_table, "Lft X Pos"]),\
                        float(df_table.at[idx_table, "Lft Y Pos"])]
            c_right = [float(df_table.at[idx_table, "Rt X Pos"]),\
                        float(df_table.at[idx_table, "Rt Y Pos"])]
            if(is_null_coord(c_left) and is_null_coord(c_right)):
                is_on_table.append([t_table, False])
            else:
                is_on_table.append([t_table, True])
        except:
            is_on_table.append([t_table, True])
        idx_table += 1
    is_on_table = get_display_interval(is_on_table, 1, df_actions)
    # print(is_on_table)

    # Merge screen and table

    # COmplete with no display


def extract_action_durations(id, figure, df_actions):
    ts = []
    for idx in df_actions.index:
        begin_ts = df_actions.at[idx,"begin"]
        end_ts = df_actions.at[idx,"end"]
        ts.append([df_actions.at[idx,"stepId"],\
            df_actions.at[idx,"actionId"],\
            begin_ts,\
            (end_ts-begin_ts)])
    csvfile = ("../data/%s_%s_actions.csv" % (id,figure))
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["stepId", "actionId", "timestamp", "duration"])
        for g in ts:
            spamwriter.writerow(g)

def extract(id, figure):
    csvfile = ("../data/%s_%s.csv" % (id,figure))
    data = pd.read_csv (csvfile)
    df_actions = pd.DataFrame(data=data)
    # print (df_actions)
    # extract_fixations(id,figure,df_actions)
    # extract_gaze_points(id,figure,df_actions)
    extract_action_durations(id,figure,df_actions)
    extract_displays_bis(id,figure,df_actions)

def main(argv):
    print("Extracting data ...")
    users = Users()
    figures = Figures()
    for id in [232968]:
        users.print_user_info(id)
        for figId in [2]:#figures.get_figures_id_list():
            print("Extract %s"%figures.get_figure_name(figId))
            try:
                extract(id, figures.get_figure_name(figId))
            except FileNotFoundError as e:
                print("Impossible to extract %s"%figures.get_figure_name(figId))
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
