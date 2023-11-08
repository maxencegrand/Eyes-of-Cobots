from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "conf/csv/actions.csv"
KEY_NAME = "name"
KEY_ID = "id"

class Action:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __str__(self):
        return self.get_name()

table = _LOAD(CSVFILE)
actions = {}

for id in _TOLIST(table, KEY_ID):
    actions[id] = Action(_GET(table, id, KEY_NAME))

def get_name(id):
    return actions[id].get_name()

def get_id(name):
    for id in get_id_list():
        if(get_name(id) == name):
            return id
    return -1
def get_id_list():
    return list(actions.keys())
