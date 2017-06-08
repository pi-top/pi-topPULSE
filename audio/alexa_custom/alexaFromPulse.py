# http://soundfile.sapp.org/doc/WaveFormat/

# https://pypi.python.org/pypi/nnresample/0.1

# https://miguelmota.com/blog/alexa-voice-service-with-curl/
# https://miguelmota.com/blog/alexa-voice-service-authentication/

# https://developer.amazon.com/public/solutions/alexa/alexa-voice-service/rest/speechrecognizer-requests

#############################
# Define functionality here #
#############################
audio_dir              = 'audio'
audio_filename         = 'output.wav'
output_audio_filename  = 'alexa.mpg'
temp_audio_filename    = audio_filename + '.tmp'
metadata_filename      = "metadata.json"
response_filename      = "response.txt"


print("Importing modules...")
import codecs
import json
import math
import requests
import signal
import ptpulse.microphone as ptpulsemic

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

# Local
DIR = os.path.dirname(os.path.realpath(__file__))
sys.path.append(DIR + "/env")
import auth
import common
print("Done...")


###################
# ALEXA FUNCTIONS #
###################
def get_avs_access_token_from_refresh_token():
    global ACCESS_TOKEN

    print("Getting new auth token...")

    data = [
        # ('grant_type', 'refresh_token'),
        # ('refresh_token', auth.REFRESH_TOKEN),
        # ('client_id', common.CLIENT_ID),
        # ('client_secret', common.CLIENT_SECRET),
        # ('redirect_uri', common.REDIRECT_URI)
    ]

    r = requests.post('https://backend.pi-top.com/api/v2/AVSRefreshToken', data=data)

    resp = r.json()
    if r.status_code == 200:
        ACCESS_TOKEN = resp['access_token']
        print("Done.")
    else:
        print("ERROR!")
        error_obj = resp['error']
        error_code = error_obj['code']
        error_msg = error_obj['message']
        print("\t" + error_code)
        print("\t" + error_msg)
        sys.exit()


def upload_to_alexa_and_save_response_to_file():
    print("Uploading audio to Alexa...")

    script_path = os.path.dirname(os.path.realpath(__file__)) + '/scripts/uploadToAlexaAndSaveResponse.sh'
    resp = subprocess.call([script_path, ACCESS_TOKEN, audio_filepath, metadata_filepath, response_filepath])

def listen_to_alexa_response():

    # Process the response to extract just the audio data
    start_writing = False
    audio_file = open(output_audio_filepath, 'w')
    with open(response_filepath) as input_file:
        for line in input_file:
            if start_writing:
                if line != "" and not line.startswith("--"):
                    audio_file.write(line)
            else:
                if "Content-Type: audio/mpeg" in line:
                    start_writing = True

    cat = subprocess.Popen(('cat', output_audio_filepath), stdout=subprocess.PIPE)
    subprocess.call(('mpg123', '-'), stdin=cat.stdout)

    cat.wait()


# Internal variables
output_audio_filepath   = DIR + "/" + audio_dir + "/" + output_audio_filename
audio_filepath          = DIR + "/" + audio_dir + "/" + audio_filename
temp_audio_filepath     = DIR + "/" + audio_dir + "/" + temp_audio_filename
metadata_filepath       = DIR + "/" + metadata_filename
response_filepath       = DIR + "/" + response_filename

ACCESS_TOKEN = ""

#####################
# LOGIC STARTS HERE #
#####################
ptpulsemic.set_sample_rate_to_16khz()
ptpulsemic.set_bit_rate_to_unsigned_16()

ptpulsemic.record()

ptpulsemic.stop()
ptpulsemic.save(audio_filepath)



print("Posting to Alexa")
get_avs_access_token_from_refresh_token()
upload_to_alexa_and_save_response_to_file()

print("Sent to Alexa - listening to response")
listen_to_alexa_response()

print("Done")
