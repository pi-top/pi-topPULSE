#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$( dirname "$DIR" )"
source $PARENT/config

AVS_ACCESS_TOKEN="${1:-$AVS_ACCESS_TOKEN}"

ENDPOINT="https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize"
METADATA_FILEPATH="$DIR/metadata.json"

if [ ! -f "$AVS_REQ_FILE" ]; then
	echo "No AVS request audio file detected - exiting"
	exit 1
fi

if [ ! -f "$METADATA_FILEPATH" ]; then
	echo "No AVS upload metadata file detected - exiting"
	exit 1
fi

if [[ "$AVS_ACCESS_TOKEN" == "" ]]; then
	echo "No AVS access token detect - exiting"
	exit 1
fi

curl -i \
  -H "Authorization: Bearer ${AVS_ACCESS_TOKEN}" \
  -F "metadata=<$METADATA_FILEPATH;type=application/json; charset=UTF-8" \
  -F "audio=<$AVS_REQ_FILE;type=audio/L16; rate=16000; channels=1" \
  -o "$AVS_RESP_TMP_FILE" \
  "$ENDPOINT"

curlSuccess=$?


# Clean up request audio file
rm "$AVS_REQ_FILE"

if [ $curlSuccess -eq 0 ]; then
	if [ -f "$AVS_RESP_TMP_FILE" ]; then

		lastLineOfResp=$(tail -n1 "$AVS_RESP_TMP_FILE")
		lastLineLength=${#lastLineOfResp}

		if [ "${lastLineOfResp:0:2}" == "--" ] && [ "${lastLineOfResp:$(($lastLineLength-3)):2}" == "--" ]; then
			sed '1,/Content-Type: audio\/mpeg/d' "$AVS_RESP_TMP_FILE" | sed '$d' > "$AVS_RESP_FILE"
			rm "$AVS_RESP_TMP_FILE"
		else
			error="$(echo "$lastLineOfResp" | jq .error)"

			if [[ "$error" != "null" ]]; then
				echo "$lastLineOfResp" | jq .error.message
			fi
		fi
	else
		echo "There was a problem finding the output file"
		exit 1
	fi
else
	echo "There was a problem downloading the response"
	exit 1
fi