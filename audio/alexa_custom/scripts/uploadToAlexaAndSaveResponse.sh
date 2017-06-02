#!/bin/bash

ENDPOINT=https://access-alexa-na.amazon.com/v1/avs/speechrecognizer/recognize
ACCESS_TOKEN=$1
AUDIO_FILEPATH=$2
METADATA_FILEPATH=$3
RESPONSE_FILEPATH=$4

# metadata.json already has "format": "audio/L16; rate=16000; channels=1"
# can we remove this here?
# what about removing the metadata.json file instead?

curl -i -H "Authorization: Bearer ${ACCESS_TOKEN}" -F "metadata=<${METADATA_FILEPATH};type=application/json; charset=UTF-8" -F "audio=<${AUDIO_FILEPATH};type=audio/L16; rate=16000; channels=1" -o "${RESPONSE_FILEPATH}" ${ENDPOINT}
