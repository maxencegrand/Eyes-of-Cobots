import cv2
import csv
from time import sleep
from pupil_apriltags import Detector
import progressbar
import argparse# Create the parser
from pathlib import Path
from time import sleep, time

def lim_coord(points, is_x = True, is_min=True):
    if(len(points) == 1):
        return points[0]
    idx = 0
    for i in range(1,len(points)):
        tmp = points[idx][0] if is_x  else points[idx][1]
        tmp_i = points[i][0] if is_x  else points[i][1]
        # print(i)
        # print(tmp)
        # print(tmp_i)
        if(is_min):
            if (tmp_i <= tmp):
                idx = i
        else:
            if (tmp_i >= tmp):
                idx = i
    return points[idx]

def get_tab_by_id(tags, id):
    for t in tags:
        if(t.tag_id == id):
            return t
    return None
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

def get_table_coordinates(tags):
    SO = [lim_coord(get_tab_by_id(tags,0).corners, is_min=False)[0],\
            lim_coord(get_tab_by_id(tags,0).corners, is_x=False, is_min=False)[1]]
    NO = [lim_coord(get_tab_by_id(tags,4).corners, is_min=False)[0],\
            lim_coord(get_tab_by_id(tags,4).corners, is_x=False)[1]]
    NE = [lim_coord(get_tab_by_id(tags,10).corners)[0],\
            lim_coord(get_tab_by_id(tags,10).corners, is_x=False)[1]]
    SE = [lim_coord(get_tab_by_id(tags,14).corners)[0],\
            lim_coord(get_tab_by_id(tags,14).corners, is_x=False, is_min=False)[1]]
    coord = [NO, SO, SE, NE]
    return coord

def draw_table(table_coord, img_):
    pta = [int(table_coord[0][0]), int(table_coord[0][1])]
    ptb = [int(table_coord[1][0]), int(table_coord[1][1])]
    ptc = [int(table_coord[2][0]), int(table_coord[2][1])]
    ptd = [int(table_coord[3][0]), int(table_coord[3][1])]

    cv2.line(img_, pta, ptb, (255, 0, 0), 4)
    cv2.line(img_, ptb, ptc, (255, 0, 0), 4)
    cv2.line(img_, ptc, ptd, (255, 0, 0), 4)
    cv2.line(img_, ptd, pta, (255, 0, 0), 4)

DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data\\recordings"
PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))

parser = argparse.ArgumentParser()# Add an argument
parser.add_argument('-user', type=str, required=True)# Parse the argument

args = parser.parse_args()

img_scene = "%s\%s\scene.jpg" % (PATH, args.user)
img_scene_markers = "%s\%s\scene_markers.jpg" % (PATH, args.user)
img_scene_table = "%s\%s\scene_table.jpg" % (PATH, args.user)
csvfile = "%s\\%s\\table_coordinates.csv" % (PATH, args.user)


# Draw markers
frame = cv2.imread(img_scene)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
detector = Detector(families="tag36h11")
results = detector.detect(gray)
draw_tags(results, frame)
cv2.imwrite(filename=img_scene_markers, img=frame)
# Compute coordinates
coord = get_table_coordinates(results)

# Draw table
draw_table(coord, frame)
cv2.imwrite(filename=img_scene_table, img=frame)

# Write CSV file
with open(csvfile, 'w',  newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Point", "x", "y"])
    writer.writerow(["NO", coord[0][0], coord[0][1]])
    writer.writerow(["SO", coord[1][0], coord[1][1]])
    writer.writerow(["SE", coord[2][0], coord[2][1]])
    writer.writerow(["NE", coord[3][0], coord[3][1]])
