from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "csv/actions.csv"
KEY_NAME = "name"
KEY_ID = "id"

class Action:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

table = _LOAD(CSVFILE)
actions = {}

for id in _TOLIST(table, KEY_ID):
    actions[i] = Color(_GET(table, id, KEY_NAME))

def get_name(id):
    return actions[i].get_name()

def get_id_list():
    return list(colors.heys())
