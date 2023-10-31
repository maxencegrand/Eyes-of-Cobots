import csv
import conf.displays as displays
import pandas as pd
from conf.point import Point

KEY_TS = "timestamp"
KEY_DISPLAY = "display"
KEY_X = "x"
KEY_Y = "y"
KEY_DURATION = "duration"
KEY_DISPERSION = "dispersion"

class Fixation:
    def __init__(self, point, dispersion, timestamp, duration, display):
        self.point = point
        self.dispersion = dispersion
        self.display = display
        self.timestamp = timestamp
        self.duration = duration

    def distance(another_point):
        return self.point.distance(timestamp)

    def __str__(self):
        str = f"{self.point} "
        str +=  f"on {displays.get_display(self.display).get_name()} "
        str += f"at {self.timestamp} and lasts {self.duration}ms"
        return str

def create_fixations(gazepoints):
    fixations = {}
    return fixations

def write_csv(csvfile, fixations):
    rows = []
    for ts in list(fixations.keys()):
        rows.append([\
            ts,\
            fixations[ts].display, \
            fixations[ts].point.x, fixations[ts].point.y],\
            fixations[ts].duration,\
            fixation[ts].dispersion)
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_TS, KEY_DISPLAY, KEY_X, KEY_Y,\
                        KEY_DURATION, KEY_DISPERSION])
        for row in rows:
            spamwriter.writerow(row)

def read_csv(csvfile):
    fixations = {}
    df = pd.DataFrame(data=pd.read_csv (csvfile))
    for idx in df.index:
        ts = int(df.at[idx, KEY_TS])
        point = Point(float(df.at[idx, KEY_X]), float(df.at[idx, KEY_Y]))
        display = int(df.at[idx, KEY_DISPLAY])
        dispersion = float(df.at[idx, KEY_DISPERSION])
        duration = int(df.at[idx, KEY_DURATION])
        fixations[ts] = Fixation(point, dispersion, ts, duration, display)
    return fixations
