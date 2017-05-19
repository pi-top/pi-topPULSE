# http://soundfile.sapp.org/doc/WaveFormat/

# https://pypi.python.org/pypi/nnresample/0.1

# https://miguelmota.com/blog/alexa-voice-service-with-curl/
# https://miguelmota.com/blog/alexa-voice-service-authentication/

# https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/rest/speechrecognizer-requests


# Define functionality here
debug = True
capture_sample_rate    = 20050
capture_bit_rate       = 8
output_file            = 'output.wav'
temp_output_file       = 'output.wav.tmp'
baud_rate              = 250000


print("Importing modules...")
import math
import signal

if not debug:
    import serial

import struct
import subprocess
import sys
import termios
import time
import tty
import os
import select
from nnresample import resample
print("Done...")


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


def update_header(file_contents, pos, int_val, byte_len):
    hex_value = spaced_l_endian_hex(int_val, byte_len)
    byte_arr = hex_to_bytes(hex_value)
    file_contents = file_contents[:pos] + byte_arr + file_contents[(pos + len(byte_arr)):]
    return file_contents


def update_header_information_after_recording():
    # Update zero'd ChunkSize and Subchunk2Size
    with open(output_file, 'r') as file:
        new_file_contents = file.read()
        
        # Calculate DATA
        size_of_data = get_size(output_file) - header_length
        print("Length of DATA: " + str(size_of_data))

        if size_of_data <= 0:
            print("No DATA - removing output file!")
            os.remove(output_file)
            success = False
        else:
            Subchunk2Size = size_of_data
            ChunkSize = 36 + Subchunk2Size

            new_file_contents = update_header(new_file_contents, pos = 4, int_val = ChunkSize, byte_len = 4)
            new_file_contents = update_header(new_file_contents, pos = 40, int_val = Subchunk2Size, byte_len = 4)

            with open(temp_output_file, 'w') as tmp_file:
                tmp_file.write(new_file_contents)

            success = True

    if success:
        os.rename(temp_output_file, output_file)

    return success


def fix_file_for_alexa():
    print("Done creating WAV file")
    # ONLY RUN IF SAMPLE RATE IS NOT EQUAL TO alexa_reqd_sample_rate
    sample_rate = get_sample_rate_wav_file()
    bits_per_sample = get_bits_per_sample_wav_file()

    correct_sample_rate = (sample_rate == alexa_reqd_sample_rate)
    correct_bits_per_sample = (bits_per_sample == alexa_reqd_bits_per_sample)
    

    if correct_sample_rate == False:
        print("File sample rate: " + str(sample_rate))
        print("Required sample rate: " + str(alexa_reqd_sample_rate))
        print("Resampling...")
        # resample_wav_file()
        print("Done resampling - adjusting bit rate")
        # adjust_wav_file_bit_rate()
    
    update_header_information_for_alexa(update_sample_rate = (correct_sample_rate == False), update_bits_per_sample = (correct_bits_per_sample == False))


def get_bits_per_sample_wav_file():
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
    with open(output_file, 'rb') as file:
        file_contents = file.read()
        file_contents_header_str = file_contents[:header_length]  # Header
        stripped_file_contents_str = file_contents[header_length:]  # After Header
        wav_float_arr = []
        for ch in stripped_file_contents_str:
            hex_item = format(ord(ch), 'x')
            float_item = float(float(int(hex_item, 16)) / 127.5) - 1.0
            # print(str(hex_item).zfill(2) + " : " + str(float_item))
            wav_float_arr.append(float_item)

    # print(wav_float_arr)

    # beta : float
    #     Beta factor for Kaiser window.  Determines tradeoff between
    #     stopband attenuation and transition band width
    # L : int
    #     FIR filter order.  Determines stopband attenuation.  The higher
    #     the better, at the cost of complexity.
    # axis : int
    #     The axis of `x` that is resampled.
    resampled_wav_float_arr = resample(wav_float_arr, alexa_reqd_sample_rate, get_sample_rate_wav_file(), beta = 5.0, L = 16001, axis = 0)

    # resampled_stripped_file_contents = sig.resample(wav_float_arr, alexa_reqd_sample_rate)

    resampled_stripped_file_contents = "";
    for float_item in resampled_wav_float_arr:
        # Convert back to int
        # -1 to +1 -> 0 to 255
        int_item = int(round((float_item + 1) * 127.5))
        
        # Catch value overflow from resampling
        if int_item < 0:
            int_item = 0
        elif int_item > 255:
            int_item = 255
        
        # int to byte
        resampled_stripped_file_contents += hex_to_bytes(spaced_l_endian_hex(int_val = int_item, byte_len = 1))

    print("Writing to " + temp_output_file)
    with open(temp_output_file, 'wb') as file:
        file.write(file_contents_header_str)
        file.write(resampled_stripped_file_contents)

    print("Moving " + temp_output_file + " to " + output_file)
    os.rename(temp_output_file, output_file)



def update_header(file_contents, pos, int_val, byte_len):
    hex_value = spaced_l_endian_hex(int_val, byte_len)
    byte_arr = hex_to_bytes(hex_value)
    file_contents = file_contents[:pos] + byte_arr + file_contents[(pos + len(byte_arr)):]
    return file_contents



def adjust_wav_file_bit_rate():
    # PAD WAV CONTENT
    with open(output_file, 'r') as file:
        with open(temp_output_file, 'w') as tmp_file:
            reading = True
            header_info = file.read(header_length)
            tmp_file.write(header_info)
            
            while reading:
                wav_byte_s = file.read(1)
                if not wav_byte_s:
                    reading = False
                else:
                    wav_byte = wav_byte_s[0]
                    
                    # wav_val = int(wav_byte.encode('hex'), 16)
                    # scaled_wav_val = wav_val * 65535 / 255
                    # wav_bytes_to_write = hex_to_bytes(spaced_l_endian_hex(scaled_wav_val, byte_len = 2))
                    # tmp_file.write(wav_bytes_to_write)

                    wav_bytes_to_write = hex_to_bytes(spaced_l_endian_hex(0, byte_len = 1)) + wav_byte
                    tmp_file.write(wav_bytes_to_write)

    os.rename(temp_output_file, output_file)
    return


def update_header_information_for_alexa(update_sample_rate = False, update_bits_per_sample = False):
    if update_sample_rate or update_bits_per_sample:
        print("Setting 'bits per sample' to 16 and sample rate to 16kHz")
        with open(output_file, 'r') as file:
            new_file_contents = file.read()

            if update_sample_rate:
                SampleRate = alexa_reqd_sample_rate                                   # SampleRate
                new_file_contents = update_header(new_file_contents, pos = 24, int_val = SampleRate, byte_len = 4)

            if update_sample_rate or update_bits_per_sample:
                ByteRate = alexa_reqd_sample_rate * (alexa_reqd_bits_per_sample / 8)  # ByteRate         == SampleRate * BitsPerSample/8
                new_file_contents = update_header(new_file_contents, pos = 28, int_val = ByteRate, byte_len = 4)

            if update_bits_per_sample:
                BlockAssign = alexa_reqd_bits_per_sample / 8                          # BlockAlign       == BitsPerSample/8
                new_file_contents = update_header(new_file_contents, pos = 32, int_val = BlockAssign, byte_len = 2)

                BitsPerSample = alexa_reqd_bits_per_sample                            # BitsPerSample
                new_file_contents = update_header(new_file_contents, pos = 34, int_val = BitsPerSample, byte_len = 2)

            with open(temp_output_file, 'w') as tmp_file:
                tmp_file.write(new_file_contents)

        os.rename(temp_output_file, output_file)


def send_to_alexa():
    # This needs porting to Python
    subprocess.call(['./requestAlexa.sh'])

def get_response_from_alexa():
    with open('response.txt', 'rb') as file:
        resp = file.read()
    print(resp)


def save_wav_from_serial():
    with open(output_file, 'wb') as file:
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
    print("Fixing WAV for Alexa")
    fix_file_for_alexa()

    print("Posting to Alexa")
    send_to_alexa()

    print("Sent to Alexa - reading response")
    get_response_from_alexa()

    print("Done")


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
            print("Updating header information")
            if update_header_information_after_recording():
                do_alexa()
            else:
                print("Error - failed to fix header information")
            break