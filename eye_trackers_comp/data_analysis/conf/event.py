from conf.position import Position
from conf.block import Block
from conf.actions import get_id
class Event:
    def __init__(self, block, position, timestamp, is_correction=False):
        self.block = block
        self.position = position
        self.is_correction = is_correction
        self.timestamp = timestamp
        self.name = "Event"

    def distance_from_center(self, point):
        return self.position.distance_from_center(point)

    def minimal_distance(self, point):
        return self.position.minimal_distance(point)

    def get_rows(self, id):
        return [id, get_id(self.name), \
        self.block.color, \
        self.block.shape, \
        self.position.top_left.x, \
        self.position.top_left.y, \
        self.position.top_right.x, \
        self.position.top_right.y, \
        self.position.bottom_left.x, \
        self.position.bottom_left.y, \
        self.position.bottom_right.x, \
        self.position.bottom_right.y]

class Pick(Event):
    def __init__(self, block, origin, timestamp, is_correction=False):
        Event.__init__(self, block, origin, timestamp,\
                is_correction=is_correction)
        self.name = "pick"

    def __str__(self):
        str = f"Pick {self.block} from {self.position} at {self.timestamp}"
        return str

class Place(Event):
    def __init__(self, block, destination, timestamp, is_correction=False):
        Event.__init__(self, block, destination, timestamp,\
                is_correction=is_correction)
        self.name = "place"

    def __str__(self):
        str = f"Place {self.block} to {self.position} at {self.timestamp}"
        return str

def create_event(action_name, block, position, timestamp, is_correction=False):
    if(action_name == "pick"):
        return Pick(block, position, timestamp, is_correction=is_correction)
    elif(action_name == "place"):
        return Place(block, position, timestamp, is_correction=is_correction)
    else:
        return
