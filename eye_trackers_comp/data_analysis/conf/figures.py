from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "conf/csv/figures.csv"
KEY_NAME = "name"
KEY_ID = "id"
KEY_N_STEPS = "nSteps"
KEY_COMPLETE_NAME = "completeName"

class Figure:
    def __init__(self, name, n, complete_name):
        self.name = name
        self.n = n
        self.complete_name = complete_name

    def get_name(self):
        return self.name

    def get_complete_name(self):
        return self.complete_name

    def get_n_steps(self):
        return self.n

    def __str__(self):
        return ("%s (%s) - %d steps" % \
            (self.get_complete_name(), self.get_name(), self.get_n_steps()))

figures = {}
table = _LOAD(CSVFILE)

for id in _TOLIST(table, KEY_ID):
    figures[id] = Figure(_GET(table, id, KEY_NAME),\
            _GET(table, id, KEY_N_STEPS),_GET(table, id, KEY_COMPLETE_NAME))

def get_name(id):
    return figures[id].get_name()

def get_complete_name(id):
    return figures[id].get_complete_name()

def get_id_list():
    return list(figures.keys())

def get_figure_id(name):
    for id in get_id_list():
        if(name == get_name(id)):
            return id
    return -1
