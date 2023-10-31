from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "csv/colors.csv"
KEY_NAME = "name"
KEY_ID = "id"

class Color:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.get_name()

table = _LOAD(CSVFILE)
colors = {}

for id in _TOLIST(table, KEY_ID):
    colors[id] = Color(_GET(table, id, KEY_NAME))

def get_name(id):
    return colors[id].get_name()

def get_id_list():
    return list(colors.keys())
