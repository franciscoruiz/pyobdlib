import time

from pyobdlib.utils import scan_serial
import pyobdlib.io
import pyobdlib.sensors


class OBD_Capture():
    def __init__(self):
        self.port = None
        localtime = time.localtime(time.time())

    def connect(self):
        portnames = scan_serial()
		#portnames = ['COM6']
        print portnames
        for port in portnames:
            self.port = pyobdlib.io.OBDDevice(port, 2, 2)
            if(self.port.state == 0):
                self.port.close()
                self.port = None
            else:
                break

        if(self.port):
            print "Connected to "+self.port.port.name

    def is_connected(self):
        return self.port

    def capture_data(self):

        #Find supported sensors - by getting PIDs from OBD
        # its a string of binary 01010101010101
        # 1 means the sensor is supported
        self.supp = self.port.sensor(0)[1]
        self.supp += self.port.sensor(32)[1]
        self.supp += self.port.sensor(64)[1]
        self.supp += self.port.sensor(96)[1]
        self.supportedSensorList = []
        self.unsupportedSensorList = []

        # loop through PIDs binary
        for i in range(0, len(self.supp)):
            if self.supp[i] == "1":
                # store index of sensor and sensor object
                self.supportedSensorList.append([i+1, pyobdlib.sensors.SENSORS[i+1]])
            else:
                self.unsupportedSensorList.append([i+1, pyobdlib.sensors.SENSORS[i+1]])

        for supportedSensor in self.supportedSensorList:
            print "supported sensor index = " + str(supportedSensor[0]) + " " + str(supportedSensor[1].shortname)

        time.sleep(3)

        if(self.port is None):
            return None

if __name__ == "__main__":

    o = OBD_Capture()
    o.connect()
    time.sleep(3)
    if not o.is_connected():
        print "Not connected"
    else:
        o.capture_data()
