import datetime
from conf import Figures, Users
from os import mkdir
import sys
from pathlib import Path

DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data\\recordings"
DATAPATH2 = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data"
PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))
PATH2 = ("%s\\%s" % (str(Path.home()), DATAPATH2))

figures = Figures()

pretest = "--pretest" in sys.argv

if (pretest):
    print("[Pretest] Users creation")
else:
    print("Users creation")

id = input ("User's ID:")

path_record = ("%s\\%s" % (PATH, id))
mkdir(path_record)
for fig_id in figures.get_figures_id_list():
    fig_name = figures.get_figure_name(fig_id)
    mkdir(("%s\\%s" % (path_record, fig_name)))
path_record = ("%s\\%s" % (PATH2, id))
mkdir(path_record)
for fig_id in figures.get_figures_id_list():
    fig_name = figures.get_figure_name(fig_id)
    mkdir(("%s\\%s" % (path_record, fig_name)))
