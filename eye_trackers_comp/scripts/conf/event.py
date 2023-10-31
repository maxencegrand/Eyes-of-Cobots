from position import Position
from block import Block

class Event:
    def __init__(self, block, position, timestamp, is_correction=False):
        self.block = block
        self.position = position
        self.is_correction = is_correction

    def distance_from_center(point):
        return self.position.distance_from_center(point)

    def minimal_distance(point):
        return self.position.minimal_distance
        (point)

class Pick(Event):
    def __init__(self, block, origin, timestamp, is_correction=False):
        Event.__init__(self, block, origin, timestamp,\
                is_correction=is_correction)

class Place(Event):
    def __init__(self, block, destination, timestamp, is_correction=False):
        Event.__init__(self, block, destination, timestamp,\
                is_correction=is_correction)

def create_event(action_name, block, position, timestamp, is_correction=False):
    if(action_name == "pick"):
        return Pick(block, position, timestamp, is_correction=is_correction)
    elif(action_name == "place"):
        return Place(block, position, timestamp, is_correction=is_correction)
    else:
        return
