import pandas as pd
import csv
import sys, getopt
from conf import Users, Figures
from table_loader import _LOAD,_GET_ALL
from utils import get_csvfile, write_csv
import math
from gaze_extractor import StationaryGazeExtractor, MobileGazeExtractor

users = Users()
figures = Figures()

def get_gaze_extractor(id, figure):
    if (users.get_setup(id) == 0):
        return MobileGazeExtractor(id, figure)
    else:
        return StationaryGazeExtractor(id, figure)

def get_steps_duration(df_steps, csvfile):
    idx_first = 0
    idx_last = len(df_steps.index)-1
    data = [["timestamp", "stepId", "duration"]]
    for idx in range(0,idx_last):
        stepId = df_steps.at[idx, "stepId"]
        timestamp = df_steps.at[idx, "timestamp"]
        duration = df_steps.at[idx+1, "timestamp"] - timestamp
        data.append([timestamp, stepId, duration])
    write_csv(csvfile, data)
    return

def extract(id, figure):
    #LOAD EVENTS FILE
    df_events = _LOAD (get_csvfile(id,figure,"event"))
    print(df_events)

    #LOAD STEPS FILE
    df_steps = _LOAD (get_csvfile(id,figure,"step"))
    print(df_steps)
    get_steps_duration(df_steps, get_csvfile(id,figure,"steps_duration"))

    #GAZE DATA EXTRACTION
    extractor = get_gaze_extractor(id, figure)
    gaze_events = extractor.get_gaze_event(df_steps)
    write_csv(get_csvfile(id,figure,"gaze_event"), gaze_events)



def main(argv):
    print("Extracting data ...")
    for id in [232968]:
        users.print_user_info(id)
        for figId in [0]:#figures.get_figures_id_list():
            print("Extract %s"%figures.get_figure_name(figId))
            try:
                extract(id, figures.get_figure_name(figId))
            except FileNotFoundError as e:
                print("Impossible to extract %s"%figures.get_figure_name(figId))
                print(e)
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
