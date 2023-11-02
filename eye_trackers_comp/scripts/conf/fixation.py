import csv
import conf.displays as displays
from conf.gazepoint import Gazepoint
import pandas as pd
from conf.point import Point, centroid, vectorize
from scipy.spatial.distance import pdist
import numpy as np

KEY_TS = "timestamp"
KEY_X = "x"
KEY_Y = "y"
KEY_DURATION = "duration"
KEY_DISPERSION = "dispersion"

class FixationDetector:
    def __init__(self, min_duration=100, max_duration=300, max_dispersion=10):
        self.min_duration = min_duration
        self.max_duration = max_duration
        self.max_dispersion = max_dispersion
        self.history = {}
        self.oldest_ts = -1

    def add_gazepoint(self, gazepoint):
        #Add the new gazepoint
        self.history[gazepoint.timestamp] = gazepoint

        timestamps = list(self.history.keys())
        dur = timestamps[len(timestamps)-1] - timestamps[0]
        # remove too old gazepoints
        while(dur > self.max_duration):
            ts_to_remove = timestamps[0]
            del(self.history[ts_to_remove])
            timestamps = list(self.history.keys())
            dur = timestamps[len(timestamps)-1] - timestamps[0]

        if(dur >= self.min_duration):
            return self.extract_fixation()
        return None

    def extract_fixation(self):
        timestamps = list(self.history.keys())
        dur = timestamps[len(timestamps)-1] - timestamps[0]
        timestamp = timestamps[0]
        gazepoints = []
        for ts in timestamps:
            gazepoints.append(self.history[ts])
        center = centroid(gazepoints)
        dispersion = gaze_dispersion(gazepoints)
        if(dispersion <= self.max_dispersion):
            return Fixation(center, dispersion, timestamp, duration, gazepoints)
        return Fixation(center, dispersion, timestamp, duration, gazepoints)

class Fixation:
    def __init__(self, point, dispersion, timestamp, duration, gazepoints):
        self.point = point
        self.dispersion = dispersion
        self.timestamp = timestamp
        self.duration = duration
        self.gazepoints = gazepoints

    def __init(self, gazepoints, timestamp, duration, display):
        self.gazepoints = gazepoints
        self.timestamp = timestamp
        self.duration = duration
        self.point = centroid(gazepoints)

    def distance(another_point):
        return self.point.distance(timestamp)

    def __str__(self):
        str = f"{self.point} "
        str +=  f"on {displays.get_display(self.display).get_name()} "
        str += f"at {self.timestamp} and lasts {self.duration}ms"
        return str

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

def extract_all_fixations(\
        gazepoints, min_duration=100, max_duration=300, max_dispersion=10):
    fixations = {}
    detector = FixationDetector(min_duration, max_duration, max_dispersion)
    timestamps = list(self.history.keys())
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
