#!/usr/bin/env python3.8

import tobii_research as tr
import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
from utils import timestamp
from utils import sleep
import math
import csv

TIME_LIMIT = 2000
ORANGE_BGR = (0,165,255)

global all_data, printable_data

all_data = []
printable_data = {}

class Screen():
    def __init__(self, top=100, left=0, width=2560, height=1440):
        self.top = top
        self.left = left
        self.width = width
        self.height = height

        with mss() as sct:
            while True:
                screenShot = sct.grab({'top': self.top, 'left': self.left,
                    'width': self.width, 'height': self.height})
                img = Image.frombytes(
                    'RGB',
                    (screenShot.width, screenShot.height),
                    screenShot.rgb,
                )
                img_ = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                self.draw_timestamps(img_)
                self.draw_gazepoints(img_)
                cv2.imshow('test', img_)
                if cv2.waitKey(33) & 0xFF in (
                    ord('q'),
                    27,
                ):
                    break

    def draw_timestamps(self, img_):
        timestamps = time() * 1000
        cv2.putText(img_, ("%f" % float(timestamps)), (8*int(self.width/10),
            9*int(self.height/10)), cv2.FONT_HERSHEY_SIMPLEX, 1, ORANGE_BGR, 2)
        return

    def draw_gazepoints(self, img_):
        timestamps = time() * 1000
        to_print = []
        to_remove = []
        for t in printable_data.keys():
            if(timestamps - (t) <= TIME_LIMIT):
                to_print.append(printable_data[t])
            else:
                to_remove.append(t)
        for t in to_remove:
            del printable_data[t]

        for i in range(1,len(to_print)):
            gp0 = [int(self.width*to_print[i-1][0]),\
                int(self.height*to_print[i-1][1])]
            gp1 = [int(self.width*to_print[i][0]),\
                int(self.height*to_print[i][1])]
            cv2.line(img_, gp0, gp1, ORANGE_BGR, 2)
            cv2.circle(img_, gp1, 5, ORANGE_BGR, 3)

class Recorder:
    def __init__(self, tracker, filename="tmp.csv"):
        self.tracker = tracker
        self.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,\
                                        self.gaze_data_callback,\
                                        as_dictionary=True)
        self.filename = filename
        self.continueToGet = True


    def gaze_data_callback(self, gaze_data):
        gaze_data['timestamp'] = timestamp()
        """Fonction qui est appelée à l'acquisition de chaque frame"""
        if (gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity'] == 1):
            gaze_data['gaze_vizualisation_x'] = round(
                (gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, 2)
            gaze_data['gaze_vizualisation_y'] = round(
                (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2, 2)

        elif (gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity'] == 0):
            gaze_data['gaze_vizualisation_x'] = gaze_data['left_gaze_point_on_display_area'][0]
            gaze_data['gaze_vizualisation_y'] = gaze_data['left_gaze_point_on_display_area'][1]

        elif (gaze_data['left_gaze_point_validity'] == 0 and gaze_data['right_gaze_point_validity'] == 1):
            gaze_data['gaze_vizualisation_x'] = gaze_data['right_gaze_point_on_display_area'][0]
            gaze_data['gaze_vizualisation_y'] = gaze_data['right_gaze_point_on_display_area'][1]


        else:
            all_data.append(gaze_data)
            return

        # all_data.append([gaze_data["timestamp"], gaze_data["x"], gaze_data["y"]])
        all_data.append(gaze_data)
        printable_data[gaze_data["timestamp"]] = [gaze_data["gaze_vizualisation_x"], gaze_data["gaze_vizualisation_y"]]
        return

    def finish(self):
        print("Write data to file %s ...\n" % self.filename)
        self.tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA,\
                                        self.gaze_data_callback)
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(all_data[0].keys())
            for row in all_data:
                if len(row) > 0:
                    writer.writerow(list(row.values()))
        print("Done.\n")

def record(tracker, filename="tmp.csv"):
    recorder = Recorder(tracker, filename=filename)
    Screen()
    recorder.finish()
