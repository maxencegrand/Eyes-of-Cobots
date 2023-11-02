import pandas as pd
import csv
import sys, getopt
import stationary_transposer as stationary
import mobile_transposer as mobile
from conf.users import Users
import conf.figures as figures
import math
import extract_duration as duration
import extract_display as display
import extract_gazepoints as gz
import extract_fixations as fx


def extract(id, figure):
    csvfile = ("../data/%s/event_%s.csv" % (id,figure))
    events = pd.DataFrame(data=pd.read_csv (csvfile))
    print (events)

    csvfile = ("../data/%s/step_%s.csv" % (id,figure))
    steps = pd.DataFrame(data=pd.read_csv (csvfile))
    print (steps)

    duration.extract(id,figure,steps)
    csvfile = ("../data/%s/steps_duration_%s.csv" % (id,figure))
    steps_durations = pd.DataFrame(data=pd.read_csv (csvfile))
    print(steps_durations)

    display.extract(id,figure,steps_durations)
    csvfile = ("../data/%s/displays_%s.csv" % (id,figure))
    display_durations = pd.DataFrame(data=pd.read_csv (csvfile))
    print(display_durations)

    gz.extract(id,figure,steps_durations)
    csvfile = ("../data/%s/gazepoints_screen_%s.csv" % (id,figure))
    gazepoints = pd.DataFrame(data=pd.read_csv (csvfile))
    print(gazepoints)
    csvfile = ("../data/%s/gazepoints_table_%s.csv" % (id,figure))
    gazepoints = pd.DataFrame(data=pd.read_csv (csvfile))
    print(gazepoints)

    fx.extract(id,figure,steps_durations)
    csvfile = ("../data/%s/fixations_screen_%s.csv" % (id,figure))
    fixations = pd.DataFrame(data=pd.read_csv (csvfile))
    print(fixations)
    csvfile = ("../data/%s/fixations_table_%s.csv" % (id,figure))
    fixations = pd.DataFrame(data=pd.read_csv (csvfile))
    print(fixations)
    # fx.extract(id,figure,steps_durations)
    # csvfile = ("../data/%s/fixations_%s.csv" % (id,figure))
    # fixations = pd.DataFrame(data=pd.read_csv (csvfile))
    # print(fixations)

def main(argv):
    print("Extracting data ...")
    users = Users(pretest=True)
    for id in [8213541]:
        users.print_user_info(id)
        for figId in [0]:#figures.get_figures_id_list():
            print("Transpose %s" % figures.get_name(figId))
            if(users.get_setup(id) == 0):#Mobile data
                mobile.transpose(id, figures.get_name(figId))
            else:
                stationary.transpose(id, figures.get_name(figId))
            print("Extract %s" % figures.get_name(figId))
            try:
                extract(id, figures.get_name(figId))
            except FileNotFoundError as e:
                print(e)
                print("Impossible to extract %s"%figures.get_name(figId))
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
