import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
import tobii_research as tr
from gazerecording import record
from utils import sleep
import math
import csv

ORANGE_BGR = (0,165,255)

# class Screen():
#     def __init__(self, recorder, top=100, left=0, width=2560, height=1440):
#         self.top = top
#         self.left = left
#         self.width = width
#         self.height = height
#         recorder.set_screen(self)
#         self.gazepoints = {}
#
#         with mss() as sct:
#             while True:
#                 screenShot = sct.grab({'top': self.top, 'left': self.left,
#                     'width': self.width, 'height': self.height})
#                 img = Image.frombytes(
#                     'RGB',
#                     (screenShot.width, screenShot.height),
#                     screenShot.rgb,
#                 )
#                 img_ = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
#                 self.draw_timestamps(img_)
#                 cv2.imshow('test', img_)
#                 if cv2.waitKey(33) & 0xFF in (
#                     ord('q'),
#                     27,
#                 ):
#                     break
#
#     def draw_timestamps(self, img_):
#         timestamps = len(self.gazepoints) #time()
#         cv2.putText(img_, ("%f" % float(timestamps)), (8*int(self.width/10),
#             9*int(self.height/10)), cv2.FONT_HERSHEY_SIMPLEX, 1, ORANGE_BGR, 2)
#         return
#
#     def add_gazepoint(self, timestamp, gazepoint):
#         self.gazepoints[timestamp] = gazepoint

class Tracker:
    def __init__(self, log = 0):
        self.data = None
        print("Get tracker")
        found_eyetrackers = tr.find_all_eyetrackers()

        if(len(found_eyetrackers) == 0):
            if(log > 0):
                print("No eyetracker")
            sys.exit(1)
        else:
            self.tracker = found_eyetrackers[0]
            if(log > 0):
                print("Address: " + self.tracker.address)
                print("Model: " + self.tracker.model)
                print("Name (It's OK if this is empty): " + self.tracker.device_name)
                print("Serial number: " + self.tracker.serial_number)

    def get_track_box(self):
        track_box = self.tracker.get_track_box()
        print("Back Lower Left: {0}".format(track_box.back_lower_left))
        print("Back Lower Right: {0}".format(track_box.back_lower_right))
        print("Back Upper Left: {0}".format(track_box.back_upper_left))
        print("Back Upper Right: {0}".format(track_box.back_upper_right))
        print("Front Lower Left: {0}".format(track_box.front_lower_left))
        print("Front Lower Right: {0}".format(track_box.front_lower_right))
        print("Front Upper Left: {0}".format(track_box.front_upper_left))
        print("Front Upper Right: {0}".format(track_box.front_upper_right))

def continue_test(question, yes=True):
    while (True):
        str = input(question)
        if(str == "y" or str == "Y" or str == "yes" or str == ""):
            return yes
        elif (str == "n" or str == "N" or str == "no"):
            return not yes
            break
        else:
            print("Bad argument %s" % str)
            continue

if __name__ == '__main__':
    # print("Welcome to the eye-tracking experiment\n")
    # in_experiment = True
    # while(in_experiment):
    #     id = input("What is the participant's ID?")
    #     savedir = input("In which directory should the data be saved for the user %s?" % id)
    #     dir = "%s\%s" % (savedir, id)
    #     if os.path.isdir(dir):
    #         print("The experiment can now begin\n")
    #         run(dir=dir)
    #         in_experiment = False
    #     else:
    #         print("The %s directory does not exist\n" % dir)
    # print("\nThe experiment is over.\nThank you for your participation.\n")
    # sys.exit(0)
    tracker = Tracker()
    filename = ("%s\TOBII-%s.csv" % (dir, "test") )
    record(tracker.tracker, filename=filename)
    # Screen(recorder)
