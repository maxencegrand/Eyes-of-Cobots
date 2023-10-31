import pandas as pd
import csv
import math
import argparse# Create the parser
from pathlib import Path
# from numpy import array
# from numpy.linalg import norm

# def get_vector(rep, p):
#     v = []
#     for i in range(len(rep)):
#         v.append(p[i]-rep[i])
#     return v
#
# def get_scalar(v1,v2):
#     res = 0
#     for i in range(len(v1)):
#         res += v1[i]*v2[i]
#     return res
#
# def get_norm(p):
#     return norm(array(p))

class Transposer:
    def __init__(self, width, height, SO, NO, SE, NE):
        self.width = width
        self.height = height
        self.SO = SO
        self.NO = NO
        self.NE = NE
        self.SE = SE

    def transpose(self,A):
        if(not self.is_on_surface(A)):
            return (float("nan"), float("nan"))
        b1y = A[1]
        b1x = self.NO[0] - (self.NO[0]-self.SO[0])*\
                float((self.NO[1]-b1y)/(self.NO[1]-self.SO[1]))
        b2y = A[1]
        b2x = self.NE[0] - (self.NE[0]-self.SE[0])*\
                float((self.NE[1]-b1y)/(self.NE[1]-self.SE[1]))

        Atransposed = (float((b1x-A[0])/(b1x-b2x)),\
            float((self.NE[1]-A[1])/(self.NE[1]-self.SO[1])))
        return Atransposed

    def is_on_surface(self, A):
        if(math.isnan(A[0]) or math.isnan(A[1])):
            return False
        if(A[1] < self.SO[1] or A[1] > self.NO[1]):
            return False
        b1y = A[1]
        b1x = self.NO[0] - (self.NO[0]-self.SO[0])*\
                float((self.NO[1]-b1y)/(self.NO[1]-self.SO[1]))
        b2y = A[1]
        b2x = self.NE[0] - (self.NE[0]-self.SE[0])*\
                float((self.NE[1]-b1y)/(self.NE[1]-self.SE[1]))
        if(A[0] < b2x):
            return False
        if(A[0] > b1x):
            return False
        return True



def transpose(user, figure):
    DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data\\recordings"
    PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))
    
    # Read table coordinates
    NO = []
    SO = []
    NE = []
    SE = []
    table_coord = "%s\\%s\\table_coordinates.csv" % (PATH, user)
    with open(table_coord, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            if(row[0] == "NO"):
                NO = [float(row[1]),float(row[2])]
            elif(row[0] == "NE"):
                NE = [float(row[1]),float(row[2])]
            elif(row[0] == "SO"):
                SO = [float(row[1]),float(row[2])]
            elif(row[0] == "SE"):
                SE = [float(row[1]),float(row[2])]

    # Create transposer
    transposer = Transposer(1280,720,SO,NO,SE,NE)
    rows = [["timestamp", \
            "left_x",\
            "left_y",\
            "right_x",\
            "right_y",\
            "left_validity",\
            "right_validity"]]

    # Initial Fovio data
    datacsv = "%s\\%s\\%s\\table.csv" % (PATH, user, figure)
    df = pd.DataFrame(data=pd.read_csv(datacsv, sep = "\t", on_bad_lines='skip'))

    # Transpose Fovio data
    for i in range(len(df.index)):
        ts = int(df.at[i, "System Time"]/1000)
        try:
            c_left = [float(df.at[i, "Lft X Pos"]),\
                        float(df.at[i, "Lft Y Pos"])]
            c_left = transposer.transpose(c_left)
            c_right = [float(df.at[i, "Rt X Pos"]),\
                        float(df.at[i, "Rt Y Pos"])]
            c_right = transposer.transpose(c_right)
            val_left = int(df.at[i,"L Quality"])
            val_right = int(df.at[i,"R Quality"])
            rows.append([ts, c_left[0],c_left[1],c_right[0],c_right[1],val_left,val_right])
        except:
            rows.append([ts,\
                    float("nan"),float("nan"),float("nan"),float("nan"),\
                    0,0])

    # Transposed Fovio data CSV file
    data_transposed = "%s\\%s\\%s\\table_norm.csv" % (PATH, user, figure)

    # Write data in csv file
    with open(data_transposed, 'w',  newline='') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)
