#!/bin/bash

#########
# SETUP #
#########
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

AUDIO_FILENAME="$DIR/audio/output.wav"
METADATA_FILENAME="$DIR/metadata.json"


echo -e "Getting auth token...\c"
"$DIR/auth/refresh.sh"
echo "Done."

echo -e "Loading auth token...\c"
source "$DIR/auth/env/auth.py"

if [[ "$ACCESS_TOKEN" == "" ]]; then
	echo "No access token - go through auth process"
	exit 1
else
	echo -e "Access Token:\n$ACCESS_TOKEN"
fi
echo "Done."


##########
# UPLOAD #
##########
echo -e "Uploading audio to Alexa...\c"

resp=$(curl -s -i \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -F "metadata=<${METADATA_FILENAME};type=application/json; charset=UTF-8" \
  -F "audio=<${AUDIO_FILENAME};type=audio/L16; rate=16000; channels=1" \
  https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize \
  -o response.txt)

echo "Done."



###################
# HANDLE RESPONSE #
###################
responseFile="$DIR/response.txt"

echo "Processing Alexa response..."
echo "$resp" | validjson &> /dev/null
valid_json=$?
if [ $valid_json -eq 0 ]; then
	ERROR=$(echo "$resp" | jq '.error.message')

	if [[ "$ERROR" != "null" ]]; then
		echo "Error: $ERROR"
		if [[ -f "$responseFile" ]]; then
			rm "$responseFile"
		fi
	else
		echo "JSON response: $resp"
	fi
else
	cat "$responseFile" | http-message-parser --pick=multipart[1].body | mpg123 -
fi
