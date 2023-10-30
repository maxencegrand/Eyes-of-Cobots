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

    def get_normalized_coordinates(self, point):
        return [float(point.x/self.width), float(point.y/self.height)]

    def get_absolute_coordinates(self, point):
        return [float(point.x*self.width), float(point.y*self.height)]

    def get_name(self):
        return self.name

    def __str__(self):
        return "%s (%f,%f)" % (self.get_name(), self.width, self.height)


displays = {}
table = _LOAD(CSVFILE)

for id in _TOLIST(table, KEY_ID):
    displays[id] = Display(_GET(table, id, KEY_NAME),\
            _GET(table, id, KEY_WIDTH),_GET(table, id, KEY_HEIGHT))


def get_absolute_coordinates(point,id):
    return displays[id].get_absolute_coordinates(point)

def get_normalized_coordinates(point,id):
    return displays[id].get_absolute_coordinates(point)

def get_name(id):
    return displays[i].get_name()

def get_id_list():
    return list(displays.keys())

print("DISPLAYS")
for id in get_id_list():
    print(displays[id])
print()
