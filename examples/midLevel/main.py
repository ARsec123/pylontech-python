#!/usr/bin/python3
""" just an example to send and recveive over /dev/ttyUSB0
    on other OSes just replace e.g. by "COM3".
    This example expects you to set the DIP switches on
    the battery to 115200 Baud.
"""
# from pylontech import PylontechRS485
# from webencodings import decode++++++
# import sys
# import os
from pylontech import PylontechRS485
from pylontech import PylontechDecode
from pylontech import PylontechEncode


def battery_state():
    # device = 'COM3'
    device = "/dev/ttyUSB0"
    pylon = PylontechRS485(device=device, baud=115200)

    e = PylontechEncode()
    d = PylontechDecode()

    print("- get Charge/Discharge Management values of Battery #0:")
    pylon.send(e.getChargeDischargeManagement(battNumber=0))
    try:
        raws = pylon.receive(0.1)
        print(d.decode_header(raws[0]))
        battery_state_1 = d.decodeChargeDischargeManagementInfo()
        # print(battery_state_1)
    except Exception as ex:
        print("     " + str(ex))

    packCount = 1
    print("- get analogue values:")
    for batt in range(0, packCount, 1):
        print("  - try battery #" + str(batt))
        pylon.send(e.getAnalogValue(battNumber=batt))  # get Analog Value
        try:
            raws = pylon.receive(0.1)
            d.decode_header(raws[0])
            battery_state_2 = d.decodeAnalogValue()
            # print(battery_state_2)
        except Exception as ex:
            print("     " + str(ex))
    print("- get serial numbers:")
    for batt in range(0, packCount, 1):
        print("  - try battery #" + str(batt))
        pylon.send(e.getSerialNumber(battNumber=batt))
        try:
            raws = pylon.receive(0.1)
            d.decode_header(raws[0])
            battery_state_3 = d.decodeSerialNumber()
            # print(battery_state_3)
        except Exception as ex:
            print("     " + str(ex))

    battery_state = {}
    battery_state.update(battery_state_1)
    battery_state.update(battery_state_2)
    battery_state.update(battery_state_3)

    return battery_state
