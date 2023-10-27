import pandas as pd
import csv
import sys, getopt
from conf import Users, Figures
from table_loader import _LOAD,_GET_ALL
import math
from fovio import display, duration, gazepoints

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

    gazepoints.extract(id,figure,steps_durations)

def main(argv):
    print("Extracting data ...")
    users = Users()
    figures = Figures()
    for id in [8213541]:
        users.print_user_info(id)
        for figId in [0]:#figures.get_figures_id_list():
            print("Extract %s"%figures.get_figure_name(figId))
            try:
                extract(id, figures.get_figure_name(figId))
            except FileNotFoundError as e:
                print(e)
                print("Impossible to extract %s"%figures.get_figure_name(figId))
    print("Done")


if __name__ == "__main__":
   main(sys.argv[1:])
