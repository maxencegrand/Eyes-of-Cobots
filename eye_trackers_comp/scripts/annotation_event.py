#!/usr/bin/env python3.8

import sys, getopt
import csv
from pathlib import Path
import argparse# Create the parser

DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data"
PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))

def main():
    parser = argparse.ArgumentParser()# Add an argument
    parser.add_argument('-user', type=str, required=True)# Parse the argument
    parser.add_argument('-figure', type=str, required=True)# Parse the argument

    args = parser.parse_args()

    # path_record = "%s\\%s\\%s" % (PATH, args.user, args.figure)

    # current_step = 0
    # actions = []
    csvfile = ("%s\\%s\\%s\\event.csv" % (PATH,args.user, args.figure))
    data = []

    print("Welcome to the event annotation module")
    print("User ID: %s" % args.user)
    print("Figure: %s" % args.figure)
    print("\nData will be save in the file: %s"%csvfile)

    id_step = 0
    id_action = 0
    prev_step = -1
    previous_end = 0
    try:
        while(True):
            pick = int(input("Pick Timestamp: "))
            data.append([pick, 1])
            place = int(input("Place Timestamp: "))
            data.append([place, 2])
    except KeyboardInterrupt:
        with open(csvfile, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=',',\
                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(["timestamp", "actionId"])
            for row in data:
                spamwriter.writerow(row)

        print("Figure %s has been event-annotated for the user %s" %\
                (args.figure, args.user))

if __name__ == "__main__":
   main()
