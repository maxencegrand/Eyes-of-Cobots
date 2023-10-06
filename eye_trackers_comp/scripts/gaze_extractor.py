import pandas as pd
import csv
from conf import Users, Figures
from table_loader import _LOAD,_GET_ALL
import math

DISPLAY = {
    0:"Screen",\
    1:"Table",\
    -1:"No_Display"
}

ZONE = {
    0:"Screen",\
    1:"Right_Stock",\
    2:"Assemly_Zone",\
    3:"Left_Stock",\
    -1:"No_Zone"
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

class GazeExtractor(object):
    def __init__(self, id, figure):
        self.id = id
        self.figure = figure
        return

    def get_gaze_events(self, df_steps):
        return

    def get_gaze_position(self):
        return

class StationaryGazeExtractor(GazeExtractor):
    def __init__(self, id, figure):
        GazeExtractor.__init__(self, id, figure)
        csvfile = ("../data/recordings/%s/%s/Screen.csv" % (self.id,self.figure))
        self.df_screen = _LOAD(csvfile)
        csvfile = ("../data/recordings/%s/%s/Table.csv" % (self.id,self.figure))
        self.df_table = _LOAD(csvfile, sep="\t")

    @staticmethod
    def merge_table(table1, table2):
        merged_table = []
        idx1 = 0
        idx2 = 0
        while(idx1 < len(table1) or idx2 < len(table2)):
            if(idx2 >= len(table2)):
                merged_table.append(table1[idx1])
                idx1 +=1
            elif(idx1 >= len(table1)):
                merged_table.append(table2[idx2])
                idx2+=2
            else:
                if(table1[idx1][0] <= table2[idx2][0]):
                    merged_table.append(table1[idx1])
                    idx1 +=1
                else:
                    merged_table.append(table2[idx2])
                    idx2 +=1
        return merged_table

    def get_gaze_event(self, df_steps):
        first_ts = df_steps.at[0, "timestamp"]
        last_ts = df_steps.at[len(df_steps.index)-1, "timestamp"]

        #SCREEN EVENTS
        is_on_screen = True
        begin = 0
        end = 0
        is_first_observation = True
        screen_data = []
        for idx_screen in range( len(self.df_screen.index)):
            t_screen = self.df_screen.at[idx_screen, "timestamp"]
            end = t_screen
            # try:
            if(math.isnan(t_screen)):
                continue
            elif(t_screen < first_ts):
                continue
            elif(t_screen > last_ts):
                if(is_on_screen):
                    screen_data.append([begin, 0, end-begin])
                break
            else:
                c_left = get_coord(self.df_screen.at[idx_screen, \
                                "left_gaze_point_on_display_area"])
                c_right = get_coord(self.df_screen.at[idx_screen, \
                                "right_gaze_point_on_display_area"])
                if(is_valid_coord(c_left) or is_valid_coord(c_right)):
                    if(is_first_observation):
                        is_on_screen = True
                        begin = t_screen
                        is_first_observation=False
                    else:
                        if(not is_on_screen):
                            begin = t_screen
                            is_on_screen = True
                else:
                    if(is_first_observation):
                        is_on_screen = False
                        begin = t_screen
                        is_first_observation=False
                    else:
                        if(is_on_screen):
                            screen_data.append([begin, 0, end-begin])
                            begin = t_screen
                            is_on_screen = False

        #TABLE EVENTS
        is_on_table = True
        begin = 0
        end = 0
        is_first_observation = True
        table_data = []
        for idx_table in range(len(self.df_table.index)):
            t_table = int(self.df_table.at[idx_table, "System Time"]/1000)
            end = t_table
            # try:
            if(math.isnan(t_table)):
                continue
            elif(t_table < first_ts):
                continue
            elif(t_table > last_ts):
                if(is_on_table):
                    table_data.append([begin, 1, end-begin])
                break
            else:
                try:
                    c_left = [float(self.df_table.at[idx_table, "Lft X Pos"]),\
                                float(self.df_table.at[idx_table, "Lft Y Pos"])]
                    c_right = [float(self.df_table.at[idx_table, "Rt X Pos"]),\
                                float(self.df_table.at[idx_table, "Rt Y Pos"])]
                    if(is_null_coord(c_left) and is_null_coord(c_right)):
                        if(is_first_observation):
                            is_on_table = True
                            begin = t_table
                            is_first_observation=False
                        else:
                            if(not is_on_table):
                                begin = t_table
                                is_on_table = True
                    else:
                        if(is_first_observation):
                            is_on_table = False
                            begin = t_table
                            is_first_observation=False
                        else:
                            if(is_on_table):
                                table_data.append([begin, 1, end-begin])
                                begin = t_table
                                is_on_table = False
                except:
                    if(is_first_observation):
                        is_on_table = False
                        begin = t_table
                        is_first_observation=False
                    else:
                        if(is_on_table):
                            table_data.append([begin, 1, end-begin])
                            begin = t_table
                            is_on_table = False

        display_data = StationaryGazeExtractor.merge_table(screen_data, table_data)

        # ADD NO DISPLAY DATA
        all_timestamps = []
        for t in self.df_screen["timestamp"].tolist():
            all_timestamps.append(t)
        for t in self.df_table["System Time"].tolist():
            all_timestamps.append(int(t/1000))
        all_timestamps = sorted(all_timestamps)

        idx = 0
        no_display_data = []
        is_on_display = True
        begin = 0
        end = 0
        is_first_observation = True
        while idx < len(all_timestamps):
            ts = all_timestamps[idx]
            end = ts
            if(ts < first_ts):
                idx += 1
                continue
            elif(ts > last_ts):
                if(not is_on_display):
                    no_display_data.append([begin, -1, end-begin])
                    break
            else:
                if(ts < display_data[0][0]):
                    if(is_first_observation):
                        is_on_display = False
                        begin = ts
                        is_first_observation = False
                    else:
                        if(is_on_display):
                            is_on_display = False
                            begin = ts
                elif(ts > display_data[len(display_data)-1][0]):
                    if(is_on_display):
                        is_on_display = False
                        begin = ts
                else:
                    #check if ts is on an "on display" interval
                    is_on_display_bis = False
                    for display in display_data:
                        if(ts >= display[0] and ts <= display[0]+display[2]):
                            is_on_display_bis = True

                    if(is_on_display_bis):
                        if(is_first_observation):
                            is_on_display = True
                            begin = ts
                        else:
                            if(not is_on_display):
                                no_display_data.append([begin, -1, end-begin])
                                begin = ts
                                is_on_display = True
                    else:
                        if(is_on_display):
                            is_on_display = False
                            begin = ts
                idx+=1

        gaze_events = StationaryGazeExtractor.\
                            merge_table(display_data, no_display_data)
        gaze_events.insert(0, ["timestamp", "displayId", "duration"])
        return gaze_events

class MobileGazeExtractor(GazeExtractor):
    def __init__(self, id):
        GazeExtractor.__init__(self, id, figure)

    def get_gaze_event(self, csvfile):
        return
