import cv2
from time import sleep
from pupil_apriltags import Detector
import progressbar
import argparse# Create the parser
from pathlib import Path

DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data\\recordings"
PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))

parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('-camera', type=int, required=True)# Parse the argument
parser.add_argument('-n', type=int, required=True)# Parse the argument
parser.add_argument('-user', type=str, required=True)# Parse the argument

args = parser.parse_args()

filename = "%s\%s\scene.jpg" % (PATH, args.user)
key = cv2.waitKey(1)
webcam = cv2.VideoCapture(args.camera)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
interupt = False
sleep(2)
best = 0
bar = progressbar.ProgressBar(maxval=args.n, \
    widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
print("Search best snapshot...")
bar.start()
for i in range(args.n):
    try:
        bar.update(i+1)
        # print("Try %d..." % i)
        check, frame = webcam.read()

        # cv2.imshow("Capturing", frame)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = Detector(families="tag36h11")
        results = detector.detect(gray)
        score = len(results)
        # print("- %d tags detected" % score)
        key = cv2.waitKey(1)
        if(score >= best):
            best = score
            cv2.imwrite(filename=filename, img=frame)

    except(KeyboardInterrupt):
        print("Process Interupted")
        break

bar.finish()
print("%d tags detect in the best snapshot" % best)
print("\nTurning off camera.")
webcam.release()
print("Camera off.")
print("Program ended.")
cv2.destroyAllWindows()
