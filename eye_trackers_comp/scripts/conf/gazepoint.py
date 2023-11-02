import csv
import conf.displays as displays
import pandas as pd
from conf.point import Point

KEY_TS = "timestamp"
KEY_X = "x"
KEY_Y = "y"

class Gazepoint:
    def __init__(self, point, timestamp):
        self.point = point
        self.timestamp = timestamp

    def distance(another_point):
        return self.point.distance(timestamp)

    def __str__(self):
        str = f"{self.point} "
        str += f"at {self.timestamp}"
        return str

def write_csv(csvfile, gazepoints):
    rows = []
    for ts in list(gazepoints.keys()):
        rows.append([\
            ts, gazepoints[ts].point.x, gazepoints[ts].point.y])
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_TS, KEY_X, KEY_Y])
        for row in rows:
            spamwriter.writerow(row)

def read_csv(csvfile):
    gazepoints = {}
    df = pd.DataFrame(data=pd.read_csv (csvfile))
    for idx in df.index:
        ts = int(df.at[idx, KEY_TS])
        point = Point(float(df.at[idx, KEY_X]), float(df.at[idx, KEY_Y]))
        gazepoints[ts] = Gazepoint(point, display, ts)
    return gazepoints
