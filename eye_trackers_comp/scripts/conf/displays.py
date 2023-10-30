from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD

#Constants
CSVFILE = "csv/displays.csv"
KEY_NAME = "name"
KEY_ID = "id"
KEY_WIDTH = "width"
KEY_HEIGHT = "height"

class Display:
    def __init__(self, name, width, height):
        self.name = name
        self.width=width
        self.height=height

    def get_normalized_coordinates(self, x, y):
        return [float(x/self.width), float(y/self.height)]

    def get_absolute_coordinates(self, x, y):
        return [float(x/self.width), float(y/self.height)]

    def get_name(self):
        return self.name

displays = {}
table = _LOAD(CSVFILE)

for id in _TOLIST(table, KEY_ID):
    displays[i] = Display(_GET(table, id, KEY_NAME),\
            _GET(table, id, KEY_WIDTH),_GET(table, id, KEY_HEIGHT))

def get_absolute_coordinates(x,y,id):
    return displays[i].get_absolute_coordinates(x,y)

def get_normalized_coordinates(x,y,id):
    return displays[i].get_absolute_coordinates(x,y)

def get_name(id):
    return displays[i].get_name()

def get_id_list():
    return list(displays.heys())
