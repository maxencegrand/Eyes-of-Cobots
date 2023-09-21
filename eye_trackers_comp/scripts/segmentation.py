#!/usr/bin/env python3.8

import sys, getopt
import csv

NB_STEPS = {
    "house":9,\
    "car":6,\
    "tc":9,\
    "tsb":12
}

def add_action(step):
    id_action = input("ID action (0: read, 1:pick, 2:place): ")
    begin_frame = input("Begin frame: ")
    end_frame = input("End frame: ")
    return [step, id_action, begin_frame, end_frame]

def main(argv):
    id = ""
    figure=""
    opts, args = getopt.getopt(argv,"h:i:f:")
    for opt, arg in opts:
        if opt == '-h':
            print ('segmentation.py -id <subject identifier> -figure <figure\'s name>')
            sys.exit()
        elif opt in ("-i"):
            id = arg
        elif opt in ("-f"):
            figure = arg

    current_step = 0
    actions = []
    csvfile = ("data/%s_%s.csv" % (id,figure))
    print(csvfile)
    with open(csvfile, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(["Step id", "Action id", "Begin", "End"])
        while (current_step <= NB_STEPS[figure]):
            command = input("(Step %d / %d) [A]dd action or [N]est step\n" % \
                    (current_step, NB_STEPS[figure]))
            if(command == "A" or command == "a"):
                spamwriter.writerow(add_action(current_step))
            elif(command == "N" or command == "n"):
                current_step += 1
            else:
                print("Unknown command %s\n" % command)

if __name__ == "__main__":
   main(sys.argv[1:])
