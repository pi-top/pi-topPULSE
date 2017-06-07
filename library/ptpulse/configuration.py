# ptpulse

import smbus
import sys
import time
import math
from numpy import uint8

_i2c_bus = smbus.SMBus(1)
_device_addr = 0x24

#######################
# INTERNAL OPERATIONS #
#######################

def _get_bit_string(value):
    """INTERNAL. Get string representation of an int in binary"""

    return "{0:b}".format(value).zfill(8)


def _update_device_state_bit(bit, value):
    """INTERNAL. Set a particular device state bit to enable or disable a particular function"""

    # Bits:  0x0000
    # Index:   3210

    if bit not in [0,1,2,3]:
        print("Not a valid state bit")
        return False

    try:
        current_state = _read_device_state()
        print("Current device state: " + _get_bit_string(current_state))

    except:
        print("There was a problem getting the current device state")
        return False

    # Get the bit mask for the new state
    new_state = uint8(math.pow(2, bit))

    if value == 0:
        new_state = ~new_state

    # Check if there is anything to do
    if (value == 1 and (new_state & current_state) != 0) or (value == 0 and (~new_state & ~current_state) != 0):
        print("Mode already set, nothing to send")
        return True

    if value == 0:
        new_state = new_state & current_state
    else:
        new_state = new_state | current_state

    # Combine the old with the new and send
    return _write_device_state(new_state)


def _verify_device_state(expected_state):
    """INTERNAL. Verify that that current device state matches that expected"""

    current_state = _read_device_state()

    if expected_state == current_state:
        return True

    else:
        print("Device write verification failed. Expected: " + _get_bit_string(expected_state) + " Received: " + _get_bit_string(current_state))
        return False


def _write_device_state(state): 
    """INTERNAL. Send the state bits across the I2C bus"""

    try:
        state_to_send = 0x0F & state

        print("Writing new state:    " + _get_bit_string(state_to_send))
        _i2c_bus.write_byte_data(_device_addr, 0, state_to_send)

        return _verify_device_state(state_to_send)

    except:
        print("There was a problem writing to device")
        return False


def _read_device_state():
    """INTERNAL. Read from the I2C bus to get the current state of the pulse. Caller should handle exceptions"""
    
    try:
        current_state = _i2c_bus.read_byte(_device_addr) & 0x0F
        return uint8(current_state)

    except:
        print("There was a problem reading from the device")
        # Best to re-raise as we can't recover from this
        raise


#######################
# EXTERNAL OPERATIONS #
#######################

def reset_device_state(enable):
    """Reset the device state bits to the default enabled or disabled state"""

    state_to_send = 0x04 if enable else 0x0B
    return _write_device_state(state_to_send)


def enable_speaker(enable):
    """Set the appropriate I2C bits to enable the speaker"""
    
    return _update_device_state_bit(0, 0 if enable else 1)


def enable_eeprom(enable):
    """Set the appropriate I2C bits to enable the eeprom"""

    return _update_device_state_bit(2, 1 if enable else 0)


def enable_microphone(enable):
    """Set the appropriate I2C bits to enable the microphone"""

    return _update_device_state_bit(1, 0 if enable else 1)


def set_microphone_sample_rate_to_16khz():
    """Set the appropriate I2C bits to enable 16,000Hz recording on the microphone"""

    return _update_device_state_bit(3, 1)


def set_microphone_sample_rate_to_22khz():
    """Set the appropriate I2C bits to enable 22,050Hz recording on the microphone"""

    return _update_device_state_bit(3, 0)
