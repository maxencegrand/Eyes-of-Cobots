import pandas as pd
import csv
import sys, getopt
import stationary_transposer as stationary
import mobile_transposer as mobile
from conf.users import Users
import conf.figures as figures
import math
from conf.step import read_csv
import extract_duration as duration
import extract_display as display
import extract_gazepoints as gz
import extract_fixations as fx
import extract_distance as distance
import extract_events as ev

MOBILE = 0
STATIONARY = 0
def extract(id, figure):
    csvfile = ("../data/%s/%s/step.csv" % (id,figure))
    steps = pd.DataFrame(data=pd.read_csv (csvfile))

    duration.extract(id, figure, steps)
    csvfile = ("../data/%s/%s/steps_duration.csv" % (id,figure))
    steps_durations = pd.DataFrame(data=pd.read_csv (csvfile))
    steps = read_csv(csvfile)

    display.extract(id, figure, steps)
    csvfile = ("../data/%s/%s/displays.csv" % (id,figure))
    display_durations = pd.DataFrame(data=pd.read_csv (csvfile))

    gz.extract(id,figure, steps)
    csvfile = ("../data/%s/%s/gazepoints_screen.csv" % (id,figure))
    gazepoints = pd.DataFrame(data=pd.read_csv (csvfile))
    csvfile = ("../data/%s/%s/gazepoints_table.csv" % (id,figure))
    gazepoints = pd.DataFrame(data=pd.read_csv (csvfile))
    
    fx.extract(id,figure, steps)
    csvfile = ("../data/%s/%s/fixations_screen.csv" % (id,figure))
    fixations = pd.DataFrame(data=pd.read_csv (csvfile))
    csvfile = ("../data/%s/%s/fixations_table.csv" % (id,figure))
    fixations = pd.DataFrame(data=pd.read_csv (csvfile))
    #
    # events = ev.extract(id, figure, steps)
    # print(events)
    # distance.extract(id, figure, steps, events)

def main(argv):
    print("Extracting data ...")
    users = Users(pretest=True)
    # for id in [4439551]:
    for id in users.get_users_id_list():
        users.print_user_info(id)
        # for figId in figures.get_id_list():
        for figId in [0]:
            try:
                # print("%s" % figures.get_complete_name(figId), end="")
                print("%s" % figures.get_complete_name(figId))
                if(users.get_setup(id) == MOBILE):
                    mobile.transpose(id, figures.get_name(figId))
                else:
                    stationary.transpose(id, figures.get_name(figId))
                extract(id, figures.get_name(figId))
                print()
                sys.exit(1)
            except FileNotFoundError as e:
                print(e)
                print(" -- Error: Impossible to extract")
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
