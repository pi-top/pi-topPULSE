import subprocess
import sys
import os
import requests

ENV_PATH = os.path.dirname(os.path.abspath(__file__)) + "/auth/env"
sys.path.append(ENV_PATH)

#########
# SETUP #
#########
DIR = os.path.dirname(os.path.realpath(__file__))

AUDIO_FILENAME = DIR + "/audio/output.wav"
METADATA_FILENAME = DIR + "/metadata.json"

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
	print("Access Token:")
	print(auth.ACCESS_TOKEN)

print("Done.")


##########
# UPLOAD #
##########
print("Uploading audio to Alexa...")

subprocess.call(["curl", "-s", "-i",
	"-H", "Authorization: Bearer " + auth.ACCESS_TOKEN,
	"-F", "metadata=<" + METADATA_FILENAME + ";type=application/json;", "charset=UTF-8",
	"-F", "audio=<" + AUDIO_FILENAME + ";type=audio/L16;", "rate=16000;", "channels=1",
	"https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize",
	"-o", "response.txt"])

# endpoint = "https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize"

# r = requests.post(
# 	endpoint,
# 	headers={
# 		"Authorization": "Bearer " + auth.ACCESS_TOKEN
# 	},
# 	forms={
# 		# ???
# 	},
# 	files={
# 		# ???
# 	}
# )

# with open('response.txt', 'wb') as handle:
#     for block in response.iter_content(1024):
#         handle.write(block)

print("Done.")






# responseFile="$DIR/response.txt"

# echo "Processing Alexa response..."
# echo "$resp" | validjson &> /dev/null
# valid_json=$?
# if [ $valid_json -eq 0 ]; then
# 	ERROR=$(echo "$resp" | jq '.error.message')

# 	if [[ "$ERROR" != "null" ]]; then
# 		echo "Error: $ERROR"
# 		if [[ -f "$responseFile" ]]; then
# 			rm "$responseFile"
# 		fi
# 	else
# 		echo "JSON response: $resp"
# 	fi
# else
# 	cat "$responseFile" | http-message-parser --pick=multipart[1].body | mpg123 -
# fi





###################
# HANDLE RESPONSE #
###################
RESPONSE_FILENAME = DIR + "/response.txt"

print("Processing Alexa response...")

# echo "$resp" | validjson &> /dev/null
# valid_json=$?
# if [ $valid_json -eq 0 ]; then
	# ERROR=$(echo "$resp" | jq '.error.message')
	if ERROR != "null":
		print("Error: $ERROR")
		if os.path.isfile(RESPONSE_FILENAME):
			os.remove(RESPONSE_FILENAME)
	else:
		print("JSON response: $resp")
# else:
	subprocess.call(["cat", RESPONSE_FILENAME, "|", "http-message-parser", "--pick=multipart[1].body", "|", "mpg123", "-"])
