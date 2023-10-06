import keyboard
import time
import csv
from pathlib import Path
import argparse# Create the parser


DATAPATH = "Documents\\Eyes-of-Cobots\\eye_trackers_comp\\data"
PATH = ("%s\\%s" % (str(Path.home()), DATAPATH))

def timestamp():
    return int(round(time.time() * 1000))

class Keylogger:
    def __init__(self, csvfile="log.csv"):
        self.log = []
        self.csvfile = csvfile

    def callback(self, event):
        """
        This callback is invoked whenever a keyboard event is occured
        (i.e when a key is released in this example)
        """
        if(event.scan_code == 77):
            print(f"{timestamp()} - Next slide")
            self.log.append([timestamp(), 1])
        elif(event.scan_code == 75):
            print(f"{timestamp()} - Previous slide")
            self.log.append([timestamp(), -1])


    def start(self):
        keyboard.on_release(callback=self.callback)
        print(f"{timestamp()} - Started keylogger")
        self.log.append([timestamp(), 0])
        keyboard.wait()

    def finish(self):
        print("Write data to file %s ...\n" % self.csvfile)
        with open(self.csvfile, 'w',  newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "stepId"])
            step = 0
            for row in self.log:
                if (len(row) > 0):
                    step += row[1]
                    print([row[0], step])
                    writer.writerow([row[0], step])
        print("Done.\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()# Add an argument
    parser.add_argument('-user', type=str, required=True)# Parse the argument
    parser.add_argument('-figure', type=str, required=True)# Parse the argument
    args = parser.parse_args()

    csvfile = ("%s\\%s_steps_%s.csv" % (PATH,args.user, args.figure))

    keylogger = Keylogger(csvfile=csvfile)
    try:
        keylogger.start()
    except KeyboardInterrupt:
        keylogger.finish()
        exit(0)
