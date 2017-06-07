# microphone.py (pi-topPULSE) 
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

import signal
import os
import binascii
import serial
import time
import struct
import sys
import ptpulse.configuration
from tempfile import mkstemp
from threading import Thread

_debug = False
_continue_writing = False
_recording_thread = False
_thread_running = False
_exiting = False
_temp_file_path = ""

_sample_rate = 22050

#######################
# INTERNAL OPERATIONS #
#######################

def _debug_print(message):
	"""INTERNAL. Print messages if debug mode enabled."""

	if _debug == True:
		print(message)	


def _signal_handler(signal, frame):
	"""INTERNAL. Handles signals from the OS."""

	global _exiting

	if _exiting == False:
		_exiting = True

		if _thread_running == True:
			stop()
	
	print("\nQuitting...")
	sys.exit(0)
	

def _get_size(filename):
	"""INTERNAL. Gets the size of a file."""

	file_stats = os.stat(filename)
	return file_stats.st_size


def _from_hex(value):
	"""INTERNAL. Gets a bytearray from hex data."""

	return bytearray.fromhex(value)


def space_separated_little_endian_hex(integer_value):
	"""INTERNAL. Get an integer in format for WAV file header."""

	hex_string = struct.pack('<i', integer_value)
	temp = binascii.hexlify(hex_string).decode()
	result = ' '.join([temp[i:i+2] for i in range(0, len(temp), 2)])

	return result


def _init_header_information():
	"""INTERNAL. Create a WAV file header."""

	# LE = little endian
	# xB = x bytes

	RIFF = "52 49 46 46"
	WAVE = "57 41 56 45"
	fmt = "66 6d 74 20"
	DATA = "64 61 74 61"
	eight_2B_LE = "08 00"
	sixteen_4B_LE = "10 00 00 00"
	one_2B_LE = "01 00"

	zero_4B = "00 00 00 00"
	
	sample_rate_LE = space_separated_little_endian_hex(_sample_rate)

	header =  _from_hex(RIFF)		    # ChunkID
	header += _from_hex(zero_4B)		# chunk_size - 4 bytes (to be changed depending on length of data...)
	header += _from_hex(WAVE)		    # Format
	header += _from_hex(fmt)			# Subchunk1ID
	header += _from_hex(sixteen_4B_LE)  # Subchunk1Size (PCM = 16)
	header += _from_hex(one_2B_LE)	    # AudioFormat   (PCM = 1)
	header += _from_hex(one_2B_LE)	    # NumChannels
	header += _from_hex(sample_rate_LE) # SampleRate
	header += _from_hex(sample_rate_LE) # ByteRate (Same as SampleRate due to 1 channel, 1 byte per sample)
	header += _from_hex(one_2B_LE)	    # BlockAlign - (no. of bytes per sample)
	header += _from_hex(eight_2B_LE)	# BitsPerSample
	header += _from_hex(DATA)		    # Subchunk2ID
	header += _from_hex(zero_4B)		# Subchunk2Size - 4 bytes (to be changed depending on length of data...)

	return header


def _update_header_in_file(file, position, value):
	"""INTERNAL. Update the WAV header	"""

	hex_value = space_separated_little_endian_hex(value)
	data = binascii.unhexlify(''.join(hex_value.split()))
	
	file.seek(position)
	file.write(data)


def _finalise_wav_file(file_path):
	"""INTERNAL. Update the WAV file header with the size of the data."""

	size_of_data = _get_size(file_path) - 44

	if size_of_data <= 0:
		print("Error: No data was recorded!")
		os.remove(file_path)
	else:
		with open(file_path, 'rb+') as file:

			_debug_print("Updating header information...")

			_update_header_in_file(file, 4, size_of_data + 36)
			_update_header_in_file(file, 40, size_of_data)


def _thread_method():
	"""INTERNAL. Thread method."""

	_record_audio()


def _record_audio():
	"""INTERNAL. Open the serial port and capture audio data into a temp file."""

	global _temp_file_path

	temp_file_tuple = mkstemp()
	os.close(temp_file_tuple[0])
	_temp_file_path = temp_file_tuple[1]

	if os.path.exists('/dev/serial0'):	  	

		_debug_print("Opening serial device...")

		serial_device = serial.Serial(port = '/dev/serial0', timeout = 1, baudrate = 250000, parity = serial.PARITY_NONE, stopbits = serial.STOPBITS_ONE, bytesize = serial.EIGHTBITS)
		serial_device_open = serial_device.isOpen()

		if serial_device_open == True:
			
			try:
				_debug_print("Start recording")
				
				with open(_temp_file_path, 'wb') as file:

					_debug_print("WRITING: initial header information")
					file.write(_init_header_information())

					if serial_device.inWaiting():
						_debug_print("Flushing input and starting from scratch")
						serial_device.flushInput()

					_debug_print("WRITING: wave data")

					while _continue_writing:
						while not serial_device.inWaiting():
							time.sleep(0.01)
						
						audio_output = serial_device.read(serial_device.inWaiting())
						file.write(audio_output)
						time.sleep(0.1)

			finally:
				serial_device.close()

				_finalise_wav_file(_temp_file_path)

				_debug_print("Finished Recording.")

		else:
			print("Error: Serial port failed to open")

	else:
		print("Error: Could not find serial port - are you sure it's enabled?")


#######################
# EXTERNAL OPERATIONS #
#######################

def record():
	"""Start recording on the pi-topPULSE microphone."""

	global _thread_running
	global _continue_writing
	global _recording_thread

	if _thread_running == False:
		_thread_running = True
		_continue_writing = True
		_recording_thread = Thread(group=None, target=_thread_method)
		_recording_thread.start()
	else:
		print("Microphone is already recording!")


def stop():
	"""Stops recording audio"""

	global _thread_running
	global _continue_writing

	_continue_writing = False
	_recording_thread.join()
	_thread_running = False
	

def save(file_path, overwrite=False):
	"""Saves recorded audio to a file."""

	global _temp_file_path

	if _thread_running == False:
		if _temp_file_path != "":
			if os.path.exists(file_path) == False or overwrite == True:
				
				if os.path.exists(file_path):
					os.remove(file_path)

				os.rename(_temp_file_path, file_path)
				_temp_file_path = ""

			else:
				print("File already exists")
		else:
			print("No recorded audio data found")
	else:
		print("Microphone is still recording!")


def set_sample_rate_to_16khz():
	"""Set the appropriate I2C bits to enable 16,000Hz recording on the microphone"""

	configuration.set_microphone_sample_rate_to_16khz()


def set_sample_rate_to_22khz():
	"""Set the appropriate I2C bits to enable 22,050Hz recording on the microphone"""

	configuration.set_microphone_sample_rate_to_22khz()


#######################
# INITIALISATION 	  #
#######################

_signal = signal.signal(signal.SIGINT, _signal_handler)