#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname "$DIR")"

source "$PARENT/env/common.py"

DEVICE_SERIAL_NUMBER=123
RESPONSE_TYPE="code"
SCOPE="alexa:all"
SCOPE_DATA="{\"alexa:all\": {\"productID\": \"$DEVICE_TYPE_ID\", \"productInstanceAttributes\": {\"deviceSerialNumber\": \"${DEVICE_SERIAL_NUMBER}\"}}}"

AUTH_URL="https://www.amazon.com/ap/oa?client_id=${CLIENT_ID}&scope=$(echo $SCOPE | urlencode)&scope_data=$(echo $SCOPE_DATA | urlencode)&response_type=${RESPONSE_TYPE}&redirect_uri=$(echo $REDIRECT_URI | urlencode)"

echo "Visit ${AUTH_URL}, approve, and paste code from redirected URL here:"
read auth_code
save CODE "$auth_code" "$PARENT/env/code.py"
