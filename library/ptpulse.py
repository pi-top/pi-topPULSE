# ptpulse.py
# Copyright (C) 2017  CEED ltd.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

import os
import serial
import signal
import sys
import time
from copy import deepcopy
from threading import Timer

_initialised = False

_w = 7
_h = 7
_rotation = 0
_brightness = 1

_max_freq = 50  # Maximum update speed is 50 times per second
_update_rate = 0.1

_running = False

_gamma_correction_arr = [
    0,     0,   0,   0,   0,   0,   0,   0,
    0,     0,   0,   0,   0,   0,   0,   0,
    0,     0,   0,   0,   0,   0,   0,   0,
    0,     0,   0,   0,   1,   1,   1,   1,
    1,     1,   1,   1,   1,   1,   1,   1,
    1,     2,   2,   2,   2,   2,   2,   2,
    2,     3,   3,   3,   3,   3,   3,   3,
    4,     4,   4,   4,   4,   5,   5,   5,
    5,     6,   6,   6,   6,   7,   7,   7,
    7,     8,   8,   8,   9,   9,   9,  10,
    10,   10,  11,  11,  11,  12,  12,  13,
    13,   13,  14,  14,  15,  15,  16,  16,
    17,   17,  18,  18,  19,  19,  20,  20,
    21,   21,  22,  22,  23,  24,  24,  25,
    25,   26,  27,  27,  28,  29,  29,  30,
    31,   32,  32,  33,  34,  35,  35,  36,
    37,   38,  39,  39,  40,  41,  42,  43,
    44,   45,  46,  47,  48,  49,  50,  50,
    51,   52,  54,  55,  56,  57,  58,  59,
    60,   61,  62,  63,  64,  66,  67,  68,
    69,   70,  72,  73,  74,  75,  77,  78,
    79,   81,  82,  83,  85,  86,  87,  89,
    90,   92,  93,  95,  96,  98,  99, 101,
    102, 104, 105, 107, 109, 110, 112, 114,
    115, 117, 119, 120, 122, 124, 126, 127,
    129, 131, 133, 135, 137, 138, 140, 142,
    144, 146, 148, 150, 152, 154, 156, 158,
    160, 162, 164, 167, 169, 171, 173, 175,
    177, 180, 182, 184, 186, 189, 191, 193,
    196, 198, 200, 203, 205, 208, 210, 213,
    215, 218, 220, 223, 225, 228, 231, 233,
    236, 239, 241, 244, 247, 249, 252, 255
]

_sync = bytearray([7, 127, 127, 127, 127, 127, 127, 127,
                  127, 127, 127, 127, 127, 127, 127])

_empty = [0, 0, 0]

_empty_map = [
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty],
    [_empty, _empty, _empty, _empty, _empty, _empty, _empty]
]

_pixel_map = _empty_map


#######################
# INTERNAL OPERATIONS #
#######################
def _initialise():
    global _initialised
    if not _initialised:
        if not os.path.exists('/dev/serial0'):
            err_str = "Could not find serial port - are you sure it's enabled?"
            raise serial.serialutil.SerialException(err_str)
        serial = serial.Serial('/dev/serial0', 115200, serial.EIGHTBITS,
                               serial.PARITY_NONE, serial.STOPBITS_ONE)
        serial.isOpen()
        _initialised = true


def _get_gamma_corrected_value(original_value):
    """
    INTERNAL. Converts a brightness value from 0-255
    to the value that produces an approximately linear
    scaling to the human eye.
    """
    global _gamma_correction_arr
    return _gamma_correction_arr[original_value]


def _scale_pixel_to_brightness(original_value):
    """
    INTERNAL. Multiplies intended brightness of
    a pixel by brightness scaling factor to generate
    an adjusted value.
    """
    global _brightness
    unrounded_new_brightness = original_value * _brightness
    rounded_new_brightness = round(unrounded_new_brightness)
    int_new_brightness = int(rounded_new_brightness)
    return int_new_brightness


def _get_rotated_pixel_map():
    """
    INTERNAL.
    """
    global _pixel_map

    rotated_pixel_map = _pixel_map
    for x in range((int(_rotation / 90) + 3) % 4):
        if sys.version_info >= (3, 0):
            rotated_pixel_map = list(zip(*rotated_pixel_map[::-1]))
        else:
            rotated_pixel_map = zip(*rotated_pixel_map[::-1])

    return rotated_pixel_map


def _brightness_correct(original_value):
    """
    INTERNAL.
    """
    brightness_scaled = _scale_pixel_to_brightness(original_value)
    new_value = _get_gamma_corrected_value(brightness_scaled)
    return new_value


def _adjust_r_g_b_for_brightness_correction(r, g, b):
    """
    INTERNAL.
    """
    r = _brightness_correct(r)
    g = _brightness_correct(g)
    b = _brightness_correct(b)

    return r, g, b


def _sync_with_device():
    """
    INTERNAL.
    """
    global _sync
    _initialise()
    serial.write(_sync)


def _show_automatically():
    """
    INTERNAL.
    """
    global _running
    global _update_rate
    while _running:
        show()
        time.sleep(_update_rate)


def _flip(direction):
    global _pixel_map
    global _h
    global _w

    flipped_pixel_map = deepcopy(_pixel_map)
    for x in range(_w):
        for y in range(_h):
            if direction is "h":
                flipped_pixel_map[x][y] = _pixel_map[(_w-1)-x][y]
            elif direction is "h":
                flipped_pixel_map[x][y] = _pixel_map[x][(_h-1)-y]
            else:
                err = 'Flip direction must be [h]orizontal or [v]ertical only'
                raise ValueError(err)

    _pixel_map = flipped_pixel_map


#######################
# EXTERNAL OPERATIONS #
#######################
def brightness(new_brightness):
    global _brightness
    if new_brightness > 1 or new_brightness < 0:
        raise ValueError('Brightness level must be between 0 and 1')
    _brightness = new_brightness


def get_brightness():
    global _brightness
    return _brightness


def rotation(new_rotation=0):
    global _rotation
    if new_rotation in [0, 90, 180, 270]:
        _rotation = new_rotation
        return True
    else:
        raise ValueError('Rotation: 0, 90, 180 or 270 degrees only')


def flip_h():
    _flip("h")


def flip_v():
    _flip("v")


def get_shape():
    global _w
    global _h
    return (_w, _h)


def get_pixel(x, y):
    global _pixel_map
    return _pixel_map[x][y]


def set_pixel(x, y, r, g, b):
    global _pixel_map
    r, g, b = _adjust_r_g_b_for_brightness_correction(r, g, b)
    _pixel_map[x][y] = [r, g, b]


def set_all(r, g, b):
    global _pixel_map
    global _w
    global _h
    _pixel_map = []

    for x in range(_w):
        row = []
        for y in range(_h):
            r, g, b = _adjust_r_g_b_for_brightness_correction(r, g, b)

            arr = [r, g, b]
            row.append(arr)

        _pixel_map.append(row)


def show():
    global _pixel_map
    global _rotation
    _sync_with_device()

    rotated_pixel_map = _get_rotated_pixel_map()

    # For each col
    for x in range(_w):
        # Get col's frame buffer
        pixel_map_buffer = chr(x)
        # For each pixel
        for y in range(_h):
            # |XX|G0|G1|R0|R1|R2|R3|R4|
            # |G2|G3|G4|B0|B1|B2|B3|B4|
            # Create 5-bit colour vals; split green into two
            rgb = rotated_pixel_map[x][y]
            r = rgb[0]
            g = rgb[1]
            b = rgb[2]
            byte0 = (r >> 3) & 0x1F
            byte1 = (b >> 3) & 0x1F
            grnb0 = (g >> 1) & 0x60
            grnb1 = (g << 2) & 0xE0
            # Combine into two bytes (5-5-5 colour)
            byte0 = (byte0 | grnb0) & 0xFF
            byte1 = (byte1 | grnb1) & 0xFF
            pixel_map_buffer += chr(byte0)
            pixel_map_buffer += chr(byte1)
        if sys.version_info >= (3, 0):
            arr = bytearray(pixel_map_buffer, 'Latin_1')
        else:
            arr = bytearray(pixel_map_buffer)

        _initialise()
        serial.write(arr)


def clear():
    _pixel_map = _empty_map


def off():
    clear()
    show()


def start(new_update_rate=0.1):
    global _update_rate
    global _running
    global _t
    if new_update_rate < (1/_max_freq):
        _update_rate = 1/_max_freq
    else:
        _update_rate = new_update_rate

    _running = True
    _t.start()


def stop():
    global _running
    global _t
    _running = False
    _t.cancel()


def signal_handler(signal, frame):
    print("\nQuitting...")
    stop()
    off()
    sys.exit(0)


##################
# INITIALISATION #
##################
signal = signal.signal(signal.SIGINT, signal_handler)

_t = Timer(_update_rate, _show_automatically)

clear()
