from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "csv/figures.csv"
KEY_NAME = "name"
KEY_ID = "id"
KEY_N_STEPS = "nSteps"
KEY_COMPLETE_NAME = "name"

class Figure:
    def __init__(self, name, n, complete_name):
        self.name = name
        self.n = n
        self.complete_name = complete_name

    def get_name(self):
        return self.name

    def get_complete_name(self):
        return self.name
