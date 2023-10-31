import csv
import displays
import pandas as pd
from point import Point

KEY_TS = "timestamp"
KEY_DISPLAY = "display"
KEY_X = "x"
KEY_Y = "y"

class Gazepoint:
    def __init__(self, point, display, timestamp):
        self.point = point
        self.display = display
        self.timestamp = timestamp

    def distance(another_point):
        return self.point.distance(timestamp)

    def __str__(self):
        str = f"{self.point} "
        str +=  f"on {displays.get_display(self.display).get_name()} "
        str += f"at {self.timestamp}"
        return str

def write_csv(csvfile, gazepoints):
    rows = []
    for ts in list(gazepoints.keys()):
        rows.append([\
            ts,\
            gazepoints[ts].display, \
            gazepoints[ts].point.x, gazepoints[ts].point.y])
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_TS, KEY_DISPLAY, KEY_X, KEY_Y])
        for row in rows:
            spamwriter.writerow(row)

def read_csv(csvfile):
    gazepoints = {}
    df = pd.DataFrame(data=pd.read_csv (csvfile))
    for idx in df.index:
        ts = int(df.at[idx, KEY_TS])
        point = Point(float(df.at[idx, KEY_X]), float(df.at[idx, KEY_Y]))
        display = int(df.at[idx, KEY_DISPLAY])
        gazepoints[ts] = Gazepoint(point, display, ts)
    return gazepoints
