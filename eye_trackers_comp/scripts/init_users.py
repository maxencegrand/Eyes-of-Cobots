import datetime
from conf import Figures, Users
from os import mkdir
import sys

figures = Figures()

pretest = "--pretest" in sys.argv

if (pretest):
    print("[Pretest] Users creation")
else:
    print("Users creation")

id = input ("User's ID:")
path_record = input("Path to record data:")

path_record2 = ("%s\\%s" % (path_record, id))
mkdir(path_record2)
for fig_id in figures.get_figures_id_list():
    fig_name = figures.get_figure_name(fig_id)
    mkdir(("%s\\%s" % (path_record2, fig_name)))
