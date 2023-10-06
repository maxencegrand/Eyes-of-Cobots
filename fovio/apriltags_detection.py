# USAGE
# python detect_apriltag.py --image images/example_01.png

# import the necessary packages
from pupil_apriltags import Detector
import cv2
from time import sleep, time

def draw_tags(tags, img_):
    for t in tags:
        # extract the bounding box (x, y)-coordinates for the AprilTag
        # and convert each of the (x, y)-coordinate pairs to integers
        (ptA, ptB, ptC, ptD) = t.corners
        ptB = (int(ptB[0]), int(ptB[1]))
        ptC = (int(ptC[0]), int(ptC[1]))
        ptD = (int(ptD[0]), int(ptD[1]))
        ptA = (int(ptA[0]), int(ptA[1]))

        # draw the bounding box of the AprilTag detection
        cv2.line(img_, ptA, ptB, (0, 0, 0), 2)
        cv2.line(img_, ptB, ptC, (0, 0, 0), 2)
        cv2.line(img_, ptC, ptD, (0, 0, 0), 2)
        cv2.line(img_, ptD, ptA, (0, 0, 0), 2)

        # draw the center (x, y)-coordinates of the AprilTag
        (cX, cY) = (int(ptA[0]), int(ptA[1]))
        # (cX, cY) = (int(r.center[0]), int(r.center[1]))
        cv2.circle(img_, (cX, cY), 5, (0, 0, 255), -1)

        # draw the tag family on the image
        tagFamily = t.tag_family.decode("utf-8")
        tagID = t.tag_id
        cv2.putText(img_, ("%d" % tagID), (int(t.center[0]-15), int(t.center[1]+15)),
            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

key = cv2. waitKey(1)
webcam = cv2.VideoCapture(0)
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
sleep(2)
for i in range(60):
    start_time = time()
    try:
        check, frame = webcam.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detector = Detector(families="tag36h11")
        results = detector.detect(gray)
        draw_tags(results, frame)
        cap = cv2.imshow("Capturing", frame)
        key = cv2.waitKey(1)

        # if key == ord('q'):
        #     webcam.release()
        #     cv2.destroyAllWindows()
        #     break
        # elif key == ord('s'):
        cv2.imwrite(filename=("scene-%d.jpg" % i), img=frame)
        webcam.release()
        print("Processing image...")
        img_ = cv2.imread("scene.jpg", cv2.IMREAD_ANYCOLOR)
        print("Converting RGB image to grayscale...")
        gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            # break

    except(KeyboardInterrupt):
        print("Turning off camera.")
        webcam.release()
        print("Camera off.")
        print("Program ended.")
        cv2.destroyAllWindows()
        break
