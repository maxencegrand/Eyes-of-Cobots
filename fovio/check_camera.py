import cv2
from time import sleep
from pupil_apriltags import Detector
import progressbar
import argparse# Create the parser

parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('-camera', type=int, required=True)# Parse the argument
args = parser.parse_args()

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(args.camera)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
interupt = False

while(True):
    try:
        check, frame = webcam.read()
        cv2.imshow("Camera - %d" % args.camera, frame)
        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    except(KeyboardInterrupt):
        print("Process Interupted")
        break

print("\nTurning off camera.")
webcam.release()
print("Camera off.")
print("Program ended.")
cv2.destroyAllWindows()
