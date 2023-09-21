import time
import tobii_research as tr
import sys
import math
from tobiiresearch.interop import interop
from tobiiresearch.implementation.Calibration import _calibration_status
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS, CALIBRATION_STATUS_FAILURE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_LEFT_EYE
from tobiiresearch.implementation.Calibration import CALIBRATION_STATUS_SUCCESS_RIGHT_EYE
import cv2

labels = {
(0.5, 0.5):"BLUE CENTER (1)",\
(0.1, 0.9):"BLUE BOTTOM LEFT (2)",\
(0.1,0.5):"BLUE LEFT (3)",\
(0.1, 0.1):"BLUE TOP LEFT (4)",\
(0.5, 0.1):"BLUE TOP (5)",\
(0.9, 0.1):"BLUE TOP RIGHT (6)",\
(0.9,0.5):"BLUE RIGHT (7)",\
(0.9,0.9):"BLUE BOTTOM RIGHT (8)",\
(0.5, 0.9):"BLUE BOTTOM (9)"
}

class Calibrator:
    def __init__(self, eyetracker):
        print("Initialize calibrator")
        # self.points_to_calibrate = [(0.5, 0.5), \
        #                             (0.1, 0.9), (0.1,0.5), (0.1, 0.1),\
        #                             (0.5, 0.1), (0.9, 0.1),\
        #                             (0.9,0.5),  (0.9,0.9), (0.5, 0.9)]
        self.points_to_calibrate = [(0.5, 0.5)]
        if eyetracker is None:
            sys.exit(1)
        self.eyetracker = eyetracker



    def calibrate_point(self, point):
        while True:
            input("Press ENTER to collect data for calibration point {0}.".format(labels[point]))

            # Wait a little for user to focus.
            time.sleep(0.7)

            x, y = (float(_) for _ in (point[0], point[1]))
            status = _calibration_status[interop.screen_based_calibration_collect_data(\
                                        self.eyetracker._EyeTracker__core_eyetracker, x, y)]
            if (status != CALIBRATION_STATUS_SUCCESS):
                print("Fail to collect data")
                continue
            else:
                break

    def calibrate(self):
        # Enter calibration mode.
        interop.calibration_enter_calibration_mode(self.eyetracker._EyeTracker__core_eyetracker)
        print("Entered calibration mode for eye tracker with serial number {0}.".format(self.eyetracker.serial_number))
        for point in self.points_to_calibrate:
            self.calibrate_point(point)
        print("Computing and applying calibration.")
        interop_result = interop.screen_based_calibration_compute_and_apply(self.eyetracker._EyeTracker__core_eyetracker)
        position = None
        calibration_points = []
        calibration_samples = []
        for interop_point in interop_result[1]:
            cur_position = interop_point.position

            if position is not None and cur_position != position:
                calibration_points.append(tr.CalibrationPoint(position, tuple(calibration_samples)))
                calibration_samples = []

            calibration_samples.append(tr.CalibrationSample(
                tr.CalibrationEyeData(interop_point.left_sample_position, interop_point.left_validity),
                tr.CalibrationEyeData(interop_point.right_sample_position, interop_point.right_validity)))

            position = cur_position

        calibration_points.append(tr.CalibrationPoint(position, tuple(calibration_samples)))

        self.calibration_result = tr.CalibrationResult(CALIBRATION_STATUS_SUCCESS, tuple(calibration_points))
        print("Compute and apply returned {0} and collected at {1} points.".
            format(self.calibration_result.status, len(self.calibration_result.calibration_points)))
        # The calibration is done. Leave calibration mode.
        interop.calibration_leave_calibration_mode(self.eyetracker._EyeTracker__core_eyetracker)
        print("Left calibration mode")
