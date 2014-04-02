# obd
# Copyright (C) 2004 Donour Sizemore
# Copyright (C) 2009 Secons Ltd.
# Copyright (C) 2013 Mark Embling
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.


import platform

import serial


def scan_serial():
    """Scan for available obd ports and return a list of available names"""

    available_ports = []

    for i in range(256):
        # Scan standard ttyS* or COM* on Windows
        try:
            s = serial.Serial(i)
            available_ports.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass

    for i in range(256):
        # Scan USB ttyACM*
        try:
            s = serial.Serial("/dev/ttyACM" + str(i))
            available_ports.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass

    for i in range(256):
        # Scan ttyUSB*
        try:
            s = serial.Serial("/dev/ttyUSB" + str(i))
            available_ports.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass

    for i in range(256):
        # Scan ttyd*
        try:
            s = serial.Serial("/dev/ttyd" + str(i))
            available_ports.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass

    # Under OS X, ELM-USB shows up as /dev/tty.usbmodemXXXX, where XXXX
    # is a changing hex string on connection; so we have to search through
    # all 64K options
    if len(platform.mac_ver()[0]) != 0:  # search only on Mac
        for i in range(65535):
            extension = hex(i).replace("0x", "", 1)
            try:
                s = serial.Serial("/dev/tty.usbmodem" + extension)
                available_ports.append(s.portstr)
                s.close()
            except serial.SerialException:
                pass

    return available_ports
