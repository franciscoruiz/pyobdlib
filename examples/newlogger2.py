import os, sys, inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

import platform
from datetime import datetime
import time
import sqlite3
import serial
import pyobdlib.io
import pyobdlib.sensors
from pyobdlib.utils import scan_serial

PORTNAME = "COM8"
LOG_SENSORS = ["rpm", "speed", "throttle_pos", "load", "temp"]

sensor_idxs = []
conn = sqlite3.connect('obdlog.db')

try:
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS Log
                 (id INTEGER PRIMARY KEY, timestamp TEXT, speed REAL, rpm REAL, load REAL, throttle REAL, coolant REAL)""")
    conn.commit()
    del c

    # Set up OBD port
    port = pyobdlib.io.OBDDevice(PORTNAME, 2, 2)
    if port.state == 0:
        port.close()
        port = None
        raise Exception("Cannot connect to %s" % PORTNAME)

    for sensor_sname in LOG_SENSORS:
        for index, e in enumerate(pyobdlib.sensors.SENSORS):
            if sensor_sname == e.shortname:
                sensor_idxs.append(index)
                print "Logging item: "+e.name
                break

    # Logging
    print "Logging started"

    while True:
        now_utc = datetime.utcnow()

        results = {}
        results["timestamp"] = str(now_utc)
        for index in sensor_idxs:
            (name, value, unit) = port.sensor(index)
            results[pyobdlib.sensors.SENSORS[index].shortname] = value;

        # Only save if the engine is running (rpm > 0)
        if results["rpm"] > 0 and results["rpm"] != "NODATA":
            tup = (results["timestamp"],
                   results["speed"],
                   results["rpm"],
                   results["load"],
                   results["throttle_pos"],
                   results["temp"])

            # Save row
            c = conn.cursor()
            c.execute("INSERT INTO Log (timestamp,speed,rpm,load,throttle,coolant) VALUES (?,?,?,?,?,?)", tup)
            conn.commit()

            print tup

        # Sleep for a moment, as it is REALLY fast
        time.sleep(0.2)

finally:
    print "Finished"
    conn.close()




