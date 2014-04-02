from contextlib import closing
import sys

from serial.tools.list_ports import comports

from obd.io import OBDDevice
from obd.obd2_codes import pcodes


def connect(device_name):
    try:
        device = OBDDevice(device_name, 2)
    except OSError:
        return None

    if device.state == 0:
        device.close()
        device = None
    else:
        print 'Connected to port', device_name

    return device


def auto_connect():
    device = None
    for device_name, device_description, hardware_id in comports():
        print 'Trying to connect to {} ({} - ID: {})'.format(
            device_description,
            device_name,
            hardware_id,
            )
        device = connect(device_name)
        if device:
            break
    return device


def _main():
    try:
        device_name = sys.argv[1]
    except IndexError:
        device_name = None

    if device_name:
        device = connect(device_name)
    else:
        device = auto_connect()

    if not device:
        sys.exit('No device found')

    with closing(device):
        for _status, dtc in device.get_dtc():
            dtc_description = pcodes[dtc]
            print '[{}] {}'.format(dtc, dtc_description)


if __name__ == '__main__':
    _main()
