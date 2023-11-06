from table_loader import _GET, _LOAD, _TOLIST, _GET_ALL, _GET_ALL_VALUES, _ADD
from conf.point import Point
from conf.position import Position

#Constants
CSVFILE_DISPLAY = "conf/csv/displays.csv"
CSVFILE_SURFACES = "conf/csv/surfaces.csv"
KEY_NAME = "name"
KEY_ID = "id"
KEY_WIDTH = "width"
KEY_HEIGHT = "height"
KEY_WIDTH_R = "widthR"
KEY_HEIGHT_R = "heightR"
KEY_X = "x"
KEY_Y = "y"

class Display:
    def __init__(self, name, width, height, widthR, heightR):
        self.name = name
        self.width=width
        self.height=height
        self.widthR=widthR
        self.heightR=heightR

    def get_normalized_coordinates(self, point):
        # print(f"{point} {self.width} {self.height} {Point(float(point.x/self.width), float(point.y/self.height))}")
        return Point(float(point.x/self.width), float(point.y/self.height))

    def get_absolute_coordinates(self, point):
        return Point(float(point.x*self.width), float(point.y*self.height))

    def get_real_coordinates(self, point):
        return Point(float(point.x*self.widthR), float(point.y*self.heightR))

    def get_real_position(self, position):
        return Position(\
            position.surface,\
            self.get_real_coordinates(\
                self.get_normalized_coordinates(position.top_left)),\
            self.get_real_coordinates(\
                self.get_normalized_coordinates(position.top_left)),\
            self.get_real_coordinates(\
                self.get_normalized_coordinates(position.top_left)),\
            self.get_real_coordinates(\
                self.get_normalized_coordinates(position.top_left)))

    def get_name(self):
        return self.name

    def __str__(self):
        return "%s (%d,%d)" % (self.get_name(), self.width, self.height)

class Surface(Display):
    def __init__(self, name, width, height, origin):
        Display.__init__(self, name, width, height, 1, 1)
        self.origin = origin

    def get_display_coordinates(self, point):
        return Point(point.x + self.origin.x, point.y + self.origin.y)

    def get_display_position(self, position):
        return Position(\
            position.surface,\
            self.get_display_coordinates(position.top_left),\
            self.get_display_coordinates(position.top_right),\
            self.get_display_coordinates(position.bottom_left),\
            self.get_display_coordinates(position.bottom_right))

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
        _GET(table, id, KEY_HEIGHT),\
        _GET(table, id, KEY_WIDTH_R),\
        _GET(table, id, KEY_HEIGHT_R))

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
