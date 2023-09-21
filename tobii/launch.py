#!/usr/bin/env python3.10

import tobii_research as tr
import sys
from calibration import Calibrator
from validation import validate
from gazerecording import record
import os

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

def run(dir="."):
    tracker = Tracker()
    calibrator = Calibrator(tracker.tracker)
    do_calibration = True
    first = True
    continue_experiment = True
    while(continue_experiment):
        while(do_calibration):
            # calibrator.calibrate()
            # validate(tracker.tracker)
            do_calibration = continue_test("\nKeep this calibration? (Y/n)", yes=False)
        csvfile = input("What is the name of the structure?")
        record(tracker.tracker, "%s/TOBII-%s.csv" % (dir, csvfile) )
        continue_experiment = continue_test("Continue experiment? (Y/n)", yes=True)
        if(continue_experiment):
            validate(tracker.tracker)
            do_calibration = continue_test("\nKeep this calibration? (Y/n)", yes=False)

if __name__ == '__main__':
    print("Welcome to the eye-tracking experiment\n")
    in_experiment = True
    while(in_experiment):
        id = input("What is the participant's ID?")
        savedir = input("In which directory should the data be saved for the user %s?" % id)
        dir = "%s\%s" % (savedir, id)
        if os.path.isdir(dir):
            print("The experiment can now begin\n")
            run(dir=dir)
            in_experiment = False
        else:
            print("The %s directory does not exist\n" % dir)
    print("\nThe experiment is over.\nThank you for your participation.\n")
    sys.exit(0)
