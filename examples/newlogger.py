from datetime import datetime
import time

from pyobdlib.utils import scan_serial
import pyobdlib.io
import pyobdlib.sensors


class OBD_Recorder():
    def __init__(self, path, log_items):
        self.port = None
        self.sensorlist = []

        localtime = time.localtime(time.time())
        filename = path+"log-"+str(localtime[0])+"-"+str(localtime[1])+"-"+str(localtime[2])+"-"+str(localtime[3])+"-"+str(localtime[4])+"-"+str(localtime[5])+".log"

        self.log_file = open(filename, "w", 128)
        self.log_file.write("Time,RPM,km/h,Throttle,Load,CoolantTemp\n");

        for item in log_items:
            self.add_log_item(item)

    def connect(self, portname = None):
        if portname is None:
            # Scan ports and try connecting
            portnames = scan_serial()
            print portnames
            for port in portnames:
                self.port = pyobdlib.io.OBDDevice(port, 2, 2)
                if(self.port.state == 0):
                    self.port.close()
                    self.port = None
                else:
                    break
        else:
            # Connect to the specified port
            self.port = pyobdlib.io.OBDDevice(portname, 2, 2)
            if(self.port.state == 0):
                self.port.close()
                self.port = None

        if(self.port):
            print "Connected to "+self.port.port.name

    def is_connected(self):
        return self.port

    def add_log_item(self, item):
        for index, e in enumerate(pyobdlib.sensors.SENSORS):
            if(item == e.shortname):
                self.sensorlist.append(index)
                print "Logging item: "+e.name
                break


    def record_data(self):
        if(self.port is None):
            return None

        print "Logging started"

        while 1:
            #localtime = datetime.now()
            #current_time = str(localtime.hour)+":"+str(localtime.minute)+":"+str(localtime.second)+"."+str(localtime.microsecond)
            current_time = str(datetime.utcnow())
            log_string = current_time
            results = {}
            for index in self.sensorlist:
                (name, value, unit) = self.port.sensor(index)
                log_string = log_string + ","+str(value)
                results[pyobdlib.sensors.SENSORS[index].shortname] = value;

            self.log_file.write(log_string+"\n")

            # Sleep for a moment, as it is REALLY fast
            time.sleep(0.2)


logitems = ["rpm", "speed", "throttle_pos", "load", "temp" ]
o = OBD_Recorder('logs', logitems)
o.connect("COM8")
if not o.is_connected():
    print "Not connected"
o.record_data()
