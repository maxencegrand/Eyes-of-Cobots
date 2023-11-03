import csv
import pandas as pd
from conf.stock import Stock
import pandas as pd
from conf.point import Point
from conf.position import create_position
from conf.event import create_event

KEY_ID = "id"
KEY_TIMESTAMP = "timestamp"
KEY_DURATION = "duration"

CSVFILE = "conf/csv/steps.csv"
KEY_STEP = "stepId"
KEY_FIGURE = "figureId"
KEY_COLOR = "colorId"
KEY_SHAPE = "shapeId"
KEY_BLOCK = "blockId"
KEY_x = "x"
KEY_Y = "y"
KEY_HORIZONTAL = "horizontal"

class Step:
    def __init__(self, id, begin, end):
        self.id = id
        self.begin = begin
        self.end = end
        self.duration = self.end - self.begin

    def is_during(self, timestamp):
        return timestamp <= self.end and timestamp >= self.begin

    def __str__(self):
        return f"Step {self.id} begins at {self.begin} and lasts {self.duration}ms"


class StepEvent:
    def __init__(self, figure, step, block, origin, destination):
        self.step = step
        self.block = block
        self.origin = origin
        self.destination = destination
        self.figure = figure

    def __str__(self):
        str = f"{self.step}: "
        str += f"{self.block} "
        str += f"{self.origin} -> {self.destination}"
        return str

def get_all_step_events(figureId, steps):
    stock = Stock()
    events = pd.DataFrame(data=pd.read_csv (CSVFILE))
    ses = []
    for idx in events.index:
        figure = int(events.at[idx, KEY_FIGURE])
        if(figure == figureId):
            id = int(events.at[idx, KEY_STEP])
            horizontal = int(events.at[idx, KEY_HORIZONTAL])
            block = stock.get_block(\
                    events.at[idx, KEY_BLOCK],\
                    events.at[idx, KEY_SHAPE],\
                    events.at[idx, KEY_COLOR])
            origin = stock.get_position(\
                    events.at[idx, KEY_BLOCK],\
                    events.at[idx, KEY_SHAPE],\
                    events.at[idx, KEY_COLOR])
            point_destination = \
                    Point(int(events.at[idx, KEY_x]), int(events.at[idx, KEY_Y]))
            destination = create_position(block, point_destination, horizontal, 2)#REPLACE 2
            se = StepEvent(figure, steps[id], block, origin, destination)
            ses.append(se)
    return ses

def get_step_event_from_timestamp(timestamp, step_events):
    for se in step_events:
        if(se.step.is_during(timestamp)):
            return se
    return None

def get_event(timestamp, action, step_events):
    se = get_step_event_from_timestamp(timestamp, step_events)
    # print(timestamp)
    event = create_event(action, se.block,\
            se.origin if(action == "pick") else se.destination,\
            timestamp)
    return event

def get_step(timestamp, steps):
    for step in steps:
        if(step.is_during(timestamp)):
            return step
    return None

def ids(self, steps):
    ids = []
    for step in steps:
        ids.append(step.id)
    return ids

def write_csv(steps, csvfile):
    rows = []
    for step in steps:
        rows.append([step.id, step.begin, step.duration])
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_ID, KEY_TIMESTAMP, KEY_DURATION])
        for row in rows:
            spamwriter.writerow(row)

def read_csv(csvfile):
    steps = []
    df = pd.DataFrame(data=pd.read_csv (csvfile))
    for idx in df.index:
        timestamp = int(df.at[idx, KEY_TIMESTAMP])
        id = int(df.at[idx, KEY_ID])
        duration = int(df.at[idx, KEY_DURATION])
        steps.append(Step(id, timestamp, timestamp+duration))
    return steps
