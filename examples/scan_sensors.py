from contextlib import closing
import sys

from serial.tools.list_ports import comports

from obd.io import OBDDevice


_SENSOR_SUPPORT_SENSOR_INDEXES = (0, 32, 64, 96)


def _get_sensor_support_PIDs(device):
    sensor_support_PIDs = []
    for sensor_index in _SENSOR_SUPPORT_SENSOR_INDEXES:
        supported_sensor_PIDs = device.sensor(sensor_index)[1]
        sensor_support_PIDs.extend(supported_sensor_PIDs)
    return sensor_support_PIDs


def get_supported_sensor_indexes(device):
    supported_sensor_PIDs = _get_sensor_support_PIDs(device)
    supported_sensor_indexes = []
    for sensor_index, is_supported in enumerate(supported_sensor_PIDs, 1):
        if is_supported == "1":
            supported_sensor_indexes.append(sensor_index)
    return supported_sensor_indexes


def print_supported_sensors_values(device):
    sensor_indexes = get_supported_sensor_indexes(device)
    for sensor_index in sensor_indexes:
        name, value, unit = device.sensor(sensor_index)
        print '{} = {!s} {}'.format(name, value, unit)


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
        print_supported_sensors_values(device)


if __name__ == '__main__':
    _main()
