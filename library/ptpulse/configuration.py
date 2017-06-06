# ptpulse

import smbus

bus = smbus.SMBus(1)

EXPLOSION_ASCII = "     _.-^^---....,,--\n _--                  --_\n<                        >)\n|                         |\n \._                   _./\n    \`\`\`--. . , ; .--'''\n          | |   |\n       .-=||  | |=-.\n       `-=#$%&%$#=-'\n          | ;  :|\n _____.,-#%&$@%#&#~,._____"


def print_explosion():
    print(EXPLOSION_ASCII)


def initialise(enable):
    # Request 1 byte from slave device
    try:
        bus.read_byte(device['addr'])
    except:
        print_explosion()
        print("There was a problem initially reading from device...")
        return False

    time.sleep(0.05)

    current_device_vals = 0x0F & bus.read_byte(device['addr'])
    message = "Current state: " + str(current_device_vals)
    _debug_print(message)

    if enable:
        # Switch on
        current_device_vals = 0x00
    else:
        # Switch off
        current_device_vals = 0x0F

    sys.stdout.write("Writing " + str(0x0F & current_device_vals) + " to device... ")

    try:
        bus.write_byte_data(device['addr'], 0, 0x0F & current_device_vals)

        _debug_print("Done")

        return _verify(device, current_device_vals)
    except:
        print_explosion()
        print("There was a problem writing to device...")
        return False


def _verify(device, values_to_verify):

    _debug_print("Verifying current state... ")
    try:
        retrieved_values = bus.read_byte(device['addr'])
        if values_to_verify == (0x0F & retrieved_values):
            print("Verified")
            return True
        else:
            print_explosion()
            print("Device write verification failed...")
            return False
    except:
        print_explosion()
        print("There was a problem reading from device...")
        return False