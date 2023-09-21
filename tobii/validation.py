import time
import tobii_research as tr
import sys
import math
from utils import distance
from utils import sleep
from utils import timestamp
from tobiiresearch.interop import interop
from tobiiresearch.implementation.Calibration import _calibration_status
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS, CALIBRATION_STATUS_FAILURE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_LEFT_EYE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_RIGHT_EYE

labels = {
(0.25,0.75):"GREEN BOTTOM LEFT (A)",\
(0.25,0.25):"GREEN TOP LEFT (B)",\
(0.75,0.25):"GREEN TOP RIGHT (C)",\
(0.75,0.75):"GREEN BOTTOM RIGHT (D)"
}

global data
data = None
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
        global data
        gaze_data['timestamp'] = timestamp()
        if (gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity']):
            gaze_data['x'] = round(
                (gaze_data['left_gaze_point_on_display_area'][0] + gaze_data['right_gaze_point_on_display_area'][0]) / 2, 2)
            gaze_data['y'] = round(
                (gaze_data['left_gaze_point_on_display_area'][1] + gaze_data['right_gaze_point_on_display_area'][1]) / 2, 2)

        elif (gaze_data['left_gaze_point_validity'] == 1 and gaze_data['right_gaze_point_validity'] == 0):
            gaze_data['x'] = gaze_data['left_gaze_point_on_display_area'][0]
            gaze_data['y'] = gaze_data['left_gaze_point_on_display_area'][1]

        elif (gaze_data['left_gaze_point_validity'] == 0 and gaze_data['right_gaze_point_validity'] == 1):
            gaze_data['x'] = gaze_data['right_gaze_point_on_display_area'][0]
            gaze_data['y'] = gaze_data['right_gaze_point_on_display_area'][1]

        else:
            gaze_data['x'] = float("nan")
            gaze_data['y'] = float("nan")
        data = gaze_data
        return

def validate(tracker):
    validator = Validator(tracker)
    validator.init_callback()
    for point in labels.keys():
        str = input("\nPress ENTER to get data for validation point {0}:".format(labels[point]))
        sleep()
        print(data)
        print("Gaze position : ({0},{1})\n".format(data["x"], data["y"]))
        if(not (math.isnan(data["x"]) or math.isnan(data["y"]))):
            print("\tDistance: {0}\n".format(distance(point, [data["x"], data["y"]])))
    validator.remove_callback()
