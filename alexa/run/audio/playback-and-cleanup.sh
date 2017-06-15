#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$( dirname "$DIR" )"
source "$PARENT/config"

if [ -f "$AVS_RESP_FILE" ]; then
	mpg123 "$AVS_RESP_FILE"
	rm "$AVS_RESP_FILE"
else
	echo "No Alexa playback file found."
fi