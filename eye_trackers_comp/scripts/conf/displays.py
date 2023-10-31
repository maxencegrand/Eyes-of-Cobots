from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD
from point import Point

#Constants
CSVFILE_DISPLAY = "csv/displays.csv"
CSVFILE_SURFACES = "csv/surfaces.csv"
KEY_NAME = "name"
KEY_ID = "id"
KEY_WIDTH = "width"
KEY_HEIGHT = "height"
KEY_X = "x"
KEY_Y = "y"

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
        return "%s (%d,%d)" % (self.get_name(), self.width, self.height)

class Surface(Display):
    def __init__(self, name, width, height, origin):
        Display.__init__(self, name, width, height)
        self.origin = origin

    def get_display_coordinates(self, point):
        new_point = Point(point.x + self.width, point.y + self.height)

    def __str__(self):
        str = Display.__str__(self)
        str += f" at {self.origin}"
        return str

# Load all displays
displays = {}
table = _LOAD(CSVFILE_DISPLAY)
for id in _TOLIST(table, KEY_ID):
    displays[id] = Display(\
        _GET(table, id, KEY_NAME),\
        _GET(table, id, KEY_WIDTH),\
        _GET(table, id, KEY_HEIGHT))

def get_display(id):
    return displays[id]

def get_displays_id_list():
    return list(displays.keys())

# print("DISPLAYS")
# for id in get_displays_id_list():
#     print(get_display(id))
# print()

# Load all surfaces
surfaces = {}
table = _LOAD(CSVFILE_SURFACES)
for id in _TOLIST(table, KEY_ID):
    surfaces[id] = Surface(\
        _GET(table, id, KEY_NAME),\
        _GET(table, id, KEY_WIDTH),\
        _GET(table, id, KEY_HEIGHT),\
        Point(_GET(table, id, KEY_X), _GET(table, id, KEY_Y)))

def get_surface(id):
    return surfaces[id]

def get_surfaces_id_list():
    return list(surfaces.keys())

# print("SURFACES")
# for id in get_surfaces_id_list():
#     print(get_surface(id))
# print()
