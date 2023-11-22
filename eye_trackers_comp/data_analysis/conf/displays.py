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
KEY_WIDTH_R = "width_mm"
KEY_HEIGHT_R = "height_mm"
KEY_X = "x"
KEY_Y = "y"

ID_SCREEN = 0
ID_TABLE = 1

ID_SCREEN_SURFACE = 3

class Display:
    def __init__(self, name, width, height, width_mm, height_mm):
        self.name = name
        self.width=width
        self.height=height
        self.width_mm=width_mm
        self.height_mm=height_mm

    def get_normalized_coordinates(self, point):
        return Point(float(point.x/self.width), float(point.y/self.height))

    def get_absolute_coordinates(self, point):
        return Point(int(point.x*self.width), int(point.y*self.height))

    def get_normalized_coordinates_from_real(self, point):
        return Point(float(point.x/self.width_mm), float(point.y/self.height_mm))

    def get_real_coordinates_from_normalized(self, point):
        return Point(float(point.x*self.width_mm), float(point.y*self.height_mm))

    def get_real_coordinates_from_absolute(self, point):
        return self.get_real_coordinates_from_normalized(\
            self.get_normalized_coordinates(point))

    def get_real_position_from_normalized(self, position):
        return Position(\
            self.get_real_coordinates_from_normalized(position.top_left),\
            self.get_real_coordinates_from_normalized(position.top_right),\
            self.get_real_coordinates_from_normalized(position.bottom_left),\
            self.get_real_coordinates_from_normalized(position.bottom_right))

    def get_real_position_from_absolute(self, position):
        return Position(\
            self.get_real_coordinates_from_absolute(position.top_left),\
            self.get_real_coordinates_from_absolute(position.top_right),\
            self.get_real_coordinates_from_absolute(position.bottom_left),\
            self.get_real_coordinates_from_absolute(position.bottom_right))

    def get_normalized_position_from_real(self, position):
        return Position(\
            self.get_normalized_coordinates_from_real(position.top_left),\
            self.get_normalized_coordinates_from_real(position.top_right),\
            self.get_normalized_coordinates_from_real(position.bottom_left),\
            self.get_normalized_coordinates_from_real(position.bottom_right))

    def get_absolute_position(self, position):
        return Position(\
            self.get_absolute_coordinates(position.top_left),\
            self.get_absolute_coordinates(position.top_right),\
            self.get_absolute_coordinates(position.bottom_left),\
            self.get_absolute_coordinates(position.bottom_right))

    def get_name(self):
        return self.name

    def __str__(self):
        return "%s (%d,%d)" % (self.get_name(), self.width, self.height)

class Surface(Display):
    def __init__(self, name, width, height, origin, display):
        Display.__init__(self, name, width, height, display.width_mm, display.height_mm)
        self.origin = origin
        self.display = display

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

# Load all surfaces
surfaces = {}
table = _LOAD(CSVFILE_SURFACES)
for id in _TOLIST(table, KEY_ID):
    if(id == ID_SCREEN_SURFACE):
        surfaces[id] = Surface(\
            _GET(table, id, KEY_NAME),\
            _GET(table, id, KEY_WIDTH),\
            _GET(table, id, KEY_HEIGHT),\
            Point(_GET(table, id, KEY_X), _GET(table, id, KEY_Y)),\
            get_display(ID_SCREEN))
    else:
        surfaces[id] = Surface(\
            _GET(table, id, KEY_NAME),\
            _GET(table, id, KEY_WIDTH),\
            _GET(table, id, KEY_HEIGHT),\
            Point(_GET(table, id, KEY_X), _GET(table, id, KEY_Y)),\
            get_display(ID_TABLE))

def get_surface(id):
    return surfaces[id]

def get_surfaces_id_list():
    return list(surfaces.keys())
