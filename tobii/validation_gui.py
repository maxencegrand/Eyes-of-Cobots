import time
import tobii_research as tr
import sys
import math
from utils import distance
from utils import sleep
from utils import timestamp
from time import time
from tobiiresearch.interop import interop
from tobiiresearch.implementation.Calibration import _calibration_status
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS, CALIBRATION_STATUS_FAILURE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_LEFT_EYE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_RIGHT_EYE
import cv2
from mss import mss
from PIL import Image
import numpy as np

TIME_LIMIT = 2000
ORANGE_BGR = (0,165,255)

labels = {
(0.25,0.75):"GREEN BOTTOM LEFT (A)",\
(0.25,0.25):"GREEN TOP LEFT (B)",\
(0.75,0.25):"GREEN TOP RIGHT (C)",\
(0.75,0.75):"GREEN BOTTOM RIGHT (D)"
}

global all_data, printable_data

all_data = []
printable_data = {}

class Gui():
    def __init__(self, top=100, left=0, width=2560, height=1440):
        self.top = top
        self.left = left
        self.width = width
        self.height = height
        prev_ts = 0
        ts = timestamp()
        with mss() as sct:
            while True:
                ts = timestamp()
                if(ts - prev_ts > 100):
                    prev_ts = ts
                    screenShot = sct.grab({'top': self.top, 'left': self.left,
                        'width': self.width, 'height': self.height})
                    img = Image.frombytes(
                        'RGB',
                        (screenShot.width, screenShot.height),
                        screenShot.rgb,
                    )
                    img_ = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
                    self.draw_gazepoints(img_)
                    cv2.imshow('test', img_)
                if cv2.waitKey(33) & 0xFF in (
                    ord('q'),
                    27,
                ):
                    cv2.destroyAllWindows()
                    break


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

class Validator:
    def __init__(self, tracker):
        self.tracker = tracker
        # self.data = None

    def init_callback(self):
        self.tracker.subscribe_to(tr.EYETRACKER_GAZE_DATA,\
                                        self.gaze_data_callback,\
                                        as_dictionary=True)
    def remove_callback(self):
        self.tracker.unsubscribe_from(tr.EYETRACKER_GAZE_DATA,\
                                        self.gaze_data_callback)

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

def validate(tracker):
    validator = Validator(tracker)
    validator.init_callback()
    # for point in labels.keys():
    #     str = input("\nPress ENTER to get data for validation point {0}:".format(labels[point]))
    #     sleep()
    #     print(data)
    #     print("Gaze position : ({0},{1})\n".format(data["x"], data["y"]))
    #     if(not (math.isnan(data["x"]) or math.isnan(data["y"]))):
    #         print("\tDistance: {0}\n".format(distance(point, [data["x"], data["y"]])))
    Gui()
    validator.remove_callback()
