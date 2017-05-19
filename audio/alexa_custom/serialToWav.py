# http://soundfile.sapp.org/doc/WaveFormat/

# https://pypi.python.org/pypi/nnresample/0.1

# https://miguelmota.com/blog/alexa-voice-service-with-curl/
# https://miguelmota.com/blog/alexa-voice-service-authentication/

# https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/rest/speechrecognizer-requests


print("Importing modules...")
import math
import serial
import signal
import struct
import subprocess
import sys
import termios
import time
import tty
import os
import select
import nnresample
print("Done...")

# Define functionality here
debug = True
capture_sample_rate    = 20050
capture_bit_rate       = 8
output_file            = 'output.wav'
baud_rate              = 250000


def signal_handler(signal, frame):
    print("\nQuitting...")
    stop()
    off()
    sys.exit(0)
signal = signal.signal(signal.SIGINT, signal_handler)


def setup_term(fd, when=termios.TCSAFLUSH):
    mode = termios.tcgetattr(fd)
    mode[tty.LFLAG] = mode[tty.LFLAG] & ~(termios.ECHO | termios.ICANON)
    termios.tcsetattr(fd, when, mode)


def get_ch(timeout=0.001):
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        setup_term(fd)
        try:
            rw, wl, xl = select.select([fd], [], [], timeout)
        except select.error:
            return
        if rw:
            return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)


def update_state_from_keypress():
    global save_to_file

    char = get_ch()
    if char != None:
        print("User pressed: " + char)

    if char == '1':
        save_to_file = True
    elif char == '0':
        save_to_file = False
    elif char == 'q':
        sys.exit()

    return save_to_file


def init_serial():
    ser = serial.Serial(
        port = '/dev/serial0',
        timeout = 1,
        baudrate = baud_rate,
        parity = serial.PARITY_NONE,
        stopbits = serial.STOPBITS_ONE,
        bytesize = serial.EIGHTBITS
    )

    print("Serial is open? " + str(ser.isOpen()))

    print("Waiting for user to start recording...")


def get_size(filename):
    st = os.stat(filename)
    return st.st_size


def hex_to_bytes(value):
    return bytearray.fromhex(value)


def spaced_l_endian_hex(int_val, byte_len=None):
    min_byte_len = int(math.ceil(float(int_val.bit_length()) / 8.0))

    if byte_len < min_byte_len:
        print("Byte length not long enough to accommodate value length")
        sys.exit()
    elif byte_len == None:
        byte_len = min_byte_len

    if byte_len <= 1:
        pack_type = '<B'
    elif byte_len <= 2:
        pack_type = '<H'
    elif byte_len <= 4:
        pack_type = '<I'
    elif byte_len <= 8:
        pack_type = '<Q'
    else:
        print("Value cannot be represented in 8 bytes - exiting")
        sys.exit()

    temp = struct.pack(pack_type, int_val).encode('hex')  # No spacing between bytes
    return ' '.join([temp[i:i+2] for i in range(0, len(temp), 2)])


def init_header_information():
    RIFF = "52 49 46 46"
    WAVE = "57 41 56 45"
    fmt  = "66 6d 74 20"
    DATA = "64 61 74 61"

    header =  hex_to_bytes(RIFF)                                                # ChunkID
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 0, byte_len = 4))      # ChunkSize - 4 bytes (to be changed depending on length of data...)
    header += hex_to_bytes(WAVE)                                                # Format
    header += hex_to_bytes(fmt)                                                 # Subchunk1ID
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 16, byte_len = 4))     # Subchunk1Size (PCM = 16)
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 1, byte_len = 2))      # AudioFormat   (PCM = 1)
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 1, byte_len = 2))      # NumChannels
    header += hex_to_bytes(spaced_l_endian_hex(int_val = capture_sample_rate))  # SampleRate
    header += hex_to_bytes(spaced_l_endian_hex(int_val = capture_sample_rate))  # ByteRate (Same as SampleRate due to 1 channel, 1 byte per sample)
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 1, byte_len = 2))      # BlockAlign - (no. of bytes per sample)
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 8, byte_len = 2))      # BitsPerSample
    header += hex_to_bytes(DATA)                                                # Subchunk2ID
    header += hex_to_bytes(spaced_l_endian_hex(int_val = 0, byte_len = 4))      # Subchunk2Size - 4 bytes (to be changed depending on length of data...)

    return header


def update_header(file, pos, int_val, byte_len):
    hex_value = spaced_l_endian_hex(int_val, byte_len)
    file.seek(pos)
    file.write(hex_to_bytes(hex_value))


def update_header_information_after_recording():
    # Update zero'd ChunkSize and Subchunk2Size
    with open(output_file, 'rw+') as file:
        print("Updating header information...")

        # Calculate DATA
        size_of_data = get_size(output_file) - header_length
        print("Length of DATA: " + str(size_of_data))

        if size_of_data <= 0:
            print("No DATA - removing output file!")
            os.remove(output_file)
            return False
        else:
            Subchunk2Size = size_of_data
            ChunkSize = 36 + Subchunk2Size

            update_header(file, pos = 4, int_val = ChunkSize, byte_len = 4)
            update_header(file, pos = 40, int_val = Subchunk2Size, byte_len = 4)
            return True


def fix_file_for_alexa():
    print("Done creating WAV file")
    # ONLY RUN IF SAMPLE RATE IS NOT EQUAL TO alexa_reqd_sample_rate
    sample_rate = get_sample_rate_wav_file()
    if sample_rate != alexa_reqd_sample_rate:
        print("File sample rate: " + str(sample_rate))
        print("Required sample rate: " + str(alexa_reqd_sample_rate))
        print("Resampling...")
        resample_wav_file()
        print("Done resampling")
    
    print("Updating header info for Alexa")
    update_header_information_for_alexa()


def get_bit_rate_wav_file():
    resp = subprocess.check_output(['sox', '--info', output_file])
    lines = resp.split("\n")

    bit_rate = None
    for line in lines:
        fields = line.split(":")
        if len(fields) >= 2 and 'Precision' in fields[0]:
            bit_rate_field = fields[1]
            bit_rate = bit_rate_field.replace("-bit", "").strip()
            break

    return bit_rate


def get_sample_rate_wav_file():
    resp = subprocess.check_output(['sox', '--info', output_file])
    lines = resp.split("\n")

    sample_rate = None
    for line in lines:
        fields = line.split(":")
        if len(fields) >= 2 and 'Sample Rate' in fields[0]:
            sample_rate_field = fields[1]
            sample_rate_str = sample_rate_field.strip()
            break

    try:
        sample_rate = int(sample_rate_str)
    except ValueError as verr:
        # s does not contain anything convertible to int
        print(verr)
        sys.exit()
    except Exception as ex:
        # Exception occurred while converting to int
        print(ex)
        sys.exit()
        pass

    return sample_rate


def resample_wav_file():
    with open(output_file, 'r') as file:
        file_contents = file.read()
        stripped_file_contents = file_contents[header_length:]

    # beta : float
    #     Beta factor for Kaiser window.  Determines tradeoff between
    #     stopband attenuation and transition band width
    # L : int
    #     FIR filter order.  Determines stopband attenuation.  The higher
    #     the better, at the cost of complexity.
    # axis : int
    #     The axis of `x` that is resampled.
    resampled_stripped_file_contents = nnresample.resample(stripped_file_contents, alexa_reqd_sample_rate, get_sample_rate_wav_file(), beta = 5.0, L = 16001, axis = 0)

    with open(output_file, 'w') as file:
        file.write(resampled_stripped_file_contents)


def update_header_information_for_alexa():
    print("Done resampling - updating bits per sample to 16")
    with open(output_file, 'rw+') as file:
        ByteRate = alexa_reqd_sample_rate * alexa_reqd_bits_per_sample / 8  # ByteRate         == SampleRate * BitsPerSample/8
        BlockAssign = alexa_reqd_bits_per_sample / 8                        # BlockAlign       == BitsPerSample/8
        BitsPerSample = alexa_reqd_bits_per_sample                          # BitsPerSample
        update_header(file, pos = 28, int_val = ByteRate, byte_len = 4)
        update_header(file, pos = 34, int_val = BitsPerSample, byte_len = 2)


def send_to_alexa():
    # This needs porting to Python
    subprocess.call(['./requestAlexa.sh'])

def get_response_from_alexa():
    with open('response.txt', 'r') as file:
        resp = file.read()
    print(resp)


def save_wav_from_serial():
    with open(output_file, 'w') as file:
        print("WRITING: initial header information")
        file.write(init_header_information())
        print("WRITING: wave data")

        counter = 0
        while save_to_file:
            update_state_from_keypress()

            if not ser.inWaiting():
                print("Waiting for serial receive")

            while not ser.inWaiting():
                time.sleep(0.001)

            print("Ready to read - reading...")
            audio_output = ser.read(ser.inWaiting())
            file.write(audio_output)
            counter += len(audio_output)
            print("WAVE DATA: Byte count - " + str(counter))

    print("Finished writing raw WAV data to file")


def do_alexa():
    print("Updating header information")
    if update_header_information_after_recording():
        print("Done creating WAV file - fixing for Alexa")
        fix_file_for_alexa()

        print("Posting to Alexa")
        send_to_alexa()

        print("Sent to Alexa - reading response")
        get_response_from_alexa()

        print("Done")
    else:
        print("Error - failed to fix header information")


# Internal variables
save_to_file = False
header_length = 44
alexa_reqd_sample_rate = 16000
alexa_reqd_bits_per_sample = 16

#####################
# LOGIC STARTS HERE #
#####################
if debug:
    do_alexa()
else:
    init_serial()
    while True:
        # save to file if appropriate
        update_state_from_keypress()
        if save_to_file:
            save_wav_from_serial()
            do_alexa()
            break
