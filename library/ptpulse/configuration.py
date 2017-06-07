# ptpulse

import smbus
import sys
import time

bus = smbus.SMBus(1)
device_addr = 0x24


def set_state(enable):
    # Request 1 byte from slave device
    try:
        bus.read_byte(device_addr)
    except:
        print("There was a problem initially reading from device...")
        return False

    time.sleep(0.05)

    current_device_vals = 0x0F & bus.read_byte(device_addr)
    message = "Current state: " + str(current_device_vals)
    print(message)

    if enable:
        # Switch on
        current_device_vals = 0x04 # 0100
    else:
        # Switch off
        current_device_vals = 0x0B # 1011

    sys.stdout.write("Writing " + str(0x0F & current_device_vals) + " to device... ")

    try:
        bus.write_byte_data(device_addr, 0, 0x0F & current_device_vals)

        print("Done")

        valid = _verify(current_device_vals)

        return valid
    except:
        print("There was a problem writing to device...")
        return False


def _verify(values_to_verify):

    print("Verifying current state... ")
    try:
        retrieved_values = bus.read_byte(device_addr)
        if values_to_verify == (0x0F & retrieved_values):
            print("Verified")
            return True
        else:
            print("Device write verification failed...")
            return False
    except:
        print("There was a problem reading from device...")
        return False