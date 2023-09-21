import keyboard
import time
import csv

def timestamp():
    return int(round(time.time() * 1000))

class Keylogger:
    def __init__(self, filename="log.csv"):
        self.log = []
        self.filename = filename

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
        # start the keylogger
        keyboard.on_release(callback=self.callback)
        # start reporting the keylogs
        # self.report()
        # make a simple message
        print(f"{timestamp()} - Started keylogger")
        # block the current thread, wait until CTRL+C is pressed
        keyboard.wait()

    def finish(self):
        print("Write data to file %s ...\n" % self.filename)
        with open(self.filename, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["Timestamp", "Slide"])
            for row in self.log:
                if (len(row) > 0):
                    print(row)
                    writer.writerow(row)
        print("Done.\n")

if __name__ == "__main__":
    keylogger = Keylogger()
    try:
        keylogger.start()
    except KeyboardInterrupt:
        keylogger.finish()
        exit(0)
