import time
import serial
import signal
import struct
import sys
import os
import select
import config


# Define functionality here
sample_rate = 22050
output_file = config.MICROPHONE_OUTPUT_FILE


def space_separated_little_endian_hex(integer_value):
	temp = struct.pack('<i', integer_value).encode('hex')  # No spacing between bytes
	return ' '.join([temp[i:i+2] for i in range(0, len(temp), 2)])


def signal_handler(signal, frame):
    print("\nQuitting...")
    stop()
    off()
    sys.exit(0)
    
signal = signal.signal(signal.SIGINT, signal_handler)


def get_size(filename):
	st = os.stat(filename)
	return st.st_size


def fromhex(value):
	return bytearray.fromhex(value)

def init_header_information():
	RIFF = "52 49 46 46"
	WAVE = "57 41 56 45"
	fmt = "66 6d 74 20"
	DATA = "64 61 74 61"
	# LE = little endian
	# xB = x bytes
	eight_2B_LE = "08 00"
	sixteen_4B_LE = "10 00 00 00"
	one_2B_LE = "01 00"

	zero_4B = "00 00 00 00"
	
	header =  fromhex(RIFF)           # ChunkID
	header += fromhex(zero_4B)        # ChunkSize - 4 bytes (to be changed depending on length of data...)
	header += fromhex(WAVE)           # Format
	header += fromhex(fmt)            # Subchunk1ID
	header += fromhex(sixteen_4B_LE)  # Subchunk1Size (PCM = 16)
	header += fromhex(one_2B_LE)      # AudioFormat   (PCM = 1)
	header += fromhex(one_2B_LE)      # NumChannels
	header += fromhex(sample_rate_LE) # SampleRate
	header += fromhex(sample_rate_LE) # ByteRate (Same as SampleRate due to 1 channel, 1 byte per sample)
	header += fromhex(one_2B_LE)      # BlockAlign - (no. of bytes per sample)
	header += fromhex(eight_2B_LE)    # BitsPerSample
	header += fromhex(DATA)           # Subchunk2ID
	header += fromhex(zero_4B)        # Subchunk2Size - 4 bytes (to be changed depending on length of data...)

	return header


def update_header_in_file(file, position, value):
	hex_value = space_separated_little_endian_hex(value)
	file.seek(position)
	file.write(bytearray.fromhex(hex_value))


def update_header_information():
	# Update zero'd ChunkSize and Subchunk2Size
	with open(output_file, 'rw+') as file:
		print("Updating header information...")
		# Calculate DATA
		size_of_data = get_size(output_file) - 44
		#print("Length of DATA: " + str(size_of_data))

		if size_of_data <= 0:
			print("No DATA - removing output file!")
			os.remove(output_file)
		else:
			Subchunk2Size = size_of_data
			ChunkSize = 36 + Subchunk2Size
			
			update_header_in_file(file, 4, ChunkSize)
			update_header_in_file(file, 40, Subchunk2Size)


# Internal variables
sample_rate_LE = space_separated_little_endian_hex(sample_rate)

ser = serial.Serial(
	port = '/dev/serial0',
	timeout = 1,
	baudrate = 250000,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS
)

if ser.isOpen():
	print("Ready to record in...")
	print("3")
	time.sleep(1)
	print("2")
	time.sleep(1)
	print("1")
	time.sleep(1)
	print("RECORDING")

	start_time = int(time.time())

	with open(config.MICROPHONE_OUTPUT_FILE, 'wb') as file:
		#print("WRITING: initial header information")
		file.write(init_header_information())
		#print("WRITING: wave data")

		if ser.inWaiting():
			#print("Flushing input and starting from scratch")
			ser.flushInput()

		save_to_file = True
		while save_to_file:
			
			while not ser.inWaiting():
				time.sleep(0.001)
			
			audio_output = ser.read(ser.inWaiting())
			file.write(audio_output)

			current_time = int(time.time())
			if (current_time - start_time) > config.MICROPHONE_RECORD_TIME_S:
				print("Stopping...")
				save_to_file = False

	ser.close()
	update_header_information()
	print("Finished Recording.")

else:
	print("Serial port failed to open")

sys.exit()