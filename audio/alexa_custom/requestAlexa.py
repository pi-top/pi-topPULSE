import json
import os
import requests
import subprocess
import sys

ENV_PATH = os.path.dirname(os.path.abspath(__file__)) + "/auth/env"
sys.path.append(ENV_PATH)

DIR = os.path.dirname(os.path.realpath(__file__))

AUDIO_FILENAME = "output.wav"
AUDIO_FILEPATH = DIR + "/audio/" + AUDIO_FILENAME
METADATA_FILENAME = "metadata.json"
METADATA_FILEPATH = DIR + "/" + METADATA_FILENAME
RESPONSE_FILENAME = "response.txt"
RESPONSE_FILEPATH = DIR + "/" + RESPONSE_FILENAME

print("Getting new auth token...")
subprocess.call(DIR + "/auth/refresh.sh")
print("Done.")


print("Loading auth token...")
import auth

try:
	auth.ACCESS_TOKEN
except NameError:
	print("No access token - go through auth process")
	sys.exit(1)
else:
	print("Done")


print("Uploading audio to Alexa...")
endpoint = "https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize"

r = requests.post(
	endpoint
	, headers={
		"Authorization": "Bearer " + auth.ACCESS_TOKEN
	}
	, files={
		'metadata': (METADATA_FILENAME, open(METADATA_FILEPATH, 'rb'), 'application/json; charset=UTF-8'),
		'audio': (AUDIO_FILENAME, open(AUDIO_FILEPATH, 'rb'), 'audio/L16; rate=16000; channels=1')
	}
)

if r.status_code != 200:
	print("ERROR!")
	resp = r.json()
	error_obj = resp['error']
	error_code = error_obj['code']
	error_msg = error_obj['message']
	print("\t" + error_code)
	print("\t" + error_msg)
	sys.exit()
	
print("Processing Alexa response...")

with open(RESPONSE_FILEPATH, 'wb') as handle:
    for block in r.iter_content(1024):
        handle.write(block)

cat = subprocess.Popen(('cat', RESPONSE_FILEPATH), stdout=subprocess.PIPE)
hmp = subprocess.Popen(('http-message-parser', '--pick=multipart[1].body'), stdin=cat.stdout, stdout=subprocess.PIPE)
output = subprocess.call(('mpg123', '-'), stdin=hmp.stdout)
cat.wait()
hmp.wait()