import csv
import conf.displays as displays
from conf.gazepoint import Gazepoint, centroid
import pandas as pd
from conf.point import Point, vectorize
from scipy.spatial.distance import pdist
import numpy as np

KEY_TS = "timestamp"
KEY_X = "x"
KEY_Y = "y"
KEY_DURATION = "duration"
KEY_DISPERSION = "dispersion"
KEY_SIZE = "size"

class FixationDetector:
    def __init__(self, min_duration=100, max_duration=300, max_dispersion=.1):
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.max_dispersion = max_dispersion
        self.history = {}
        self.oldest_ts = -1

    def oldest_timestamp(self):
        return list(self.history.keys())[0]

    def newest_timestamp(self):
        return list(self.history.keys())[self.size()-1]

    def duration(self):
        return self.newest_timestamp() - self.oldest_timestamp()

    def size(self):
        return len(self.history)

    def sort_history(self):
        self.history = dict(sorted(self.history.items()))

    def remove_oldest(self):
        ts_to_remove = self.oldest_timestamp()
        del(self.history[ts_to_remove])
        self.sort_history()

    def add(self, gazepoint):
        self.history[gazepoint.timestamp] = gazepoint
        self.sort_history()

    def dispersion(self):
        if(self.size() == 1):
            return 0
        return gaze_dispersion(list(self.history.values()))

    def center(self):
        return centroid(list(self.history.values()))

    def add_gazepoint(self, gazepoint):
        #Add the new gazepoint
        self.add(gazepoint)

        # remove too old gazepoints
        while(self.duration() > self.max_duration):
            self.remove_oldest()

        if(self.size() >= 2 and self.duration() >= self.min_duration):
            return self.extract_fixation()

        return None

    def extract_fixation(self):
        if(self.dispersion() <= self.max_dispersion):
            return Fixation(\
                    self.center(),\
                    self.dispersion(),\
                    self.oldest_timestamp(),\
                    self.duration(),\
                    self.size())
        return None

class Fixation:
    def __init__(self, point, dispersion, timestamp, duration, size):
        self.point = point
        self.dispersion = dispersion
        self.timestamp = timestamp
        self.duration = duration
        self.size = size

    def __init(self, gazepoints, timestamp, duration, display):
        self.timestamp = timestamp
        self.duration = duration
        self.point = centroid(gazepoints)
        self.size = len(gazepoints)

    def distance(self, another_point):
        return self.point.distance(timestamp)

    def __str__(self):
        str = f"{self.point} "
        str += f"at {self.timestamp} and lasts {self.duration}ms"
        str += f" ( {self.size} gazepoints)"
        return str

def write_csv(csvfile, fixations):
    rows = []
    for ts in list(fixations.keys()):
        rows.append([\
            fixations[ts].timestamp, \
            fixations[ts].point.x,\
            fixations[ts].point.y,\
            fixations[ts].duration,\
            fixations[ts].dispersion,\
            fixations[ts].size])
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='\"', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow([KEY_TS, KEY_X, KEY_Y, KEY_DURATION, KEY_DISPERSION, KEY_SIZE])
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
        size = float(df.at[idx, KEY_SIZE])
        fixations[ts] = Fixation(point, dispersion, ts, display)
    return fixations

def extract_all_fixations(\
        gazepoints, min_duration=100, max_duration=500, max_dispersion=.1):
    fixations = {}
    detector = FixationDetector(min_duration, max_duration, max_dispersion)
    timestamps = list(gazepoints.keys())
    for ts in timestamps:
        fixation = detector.add_gazepoint(gazepoints[ts])
        if not fixation is None:
            fixations[fixation.timestamp] = fixation
    return fixations

def vector_dispersion(vectors):
    distances = pdist(vectors, metric="cosine")
    dispersion = np.arccos(1.0 - distances.max())
    return dispersion

def gaze_dispersion(gazepoints):
    vectors = vectorize(gazepoints)
    return vector_dispersion(vectors)
