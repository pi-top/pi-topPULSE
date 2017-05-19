#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname "$DIR")"

if [ -f "$PARENT/env/common.py" ]; then
	source "$PARENT/env/common.py"
else
	echo "No 'common' file"
	exit 1
fi

if [ -f "$PARENT/env/code.py" ]; then
	source "$PARENT/env/code.py"
else
	echo "No 'code' file - run setup_get_auth_code_url.sh"
	exit 1
fi

GRANT_TYPE="authorization_code"
DATA="code=${CODE}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&redirect_uri=$(echo ${REDIRECT_URI} | urlencode)&grant_type=${GRANT_TYPE}"

resp=$(curl -s -X POST --data "$DATA" https://api.amazon.com/auth/o2/token)

ERROR=$(echo $resp | jq '.error')

if [ ! -z "$ERROR" ] && [[ "$ERROR" != "null" ]]; then
	echo "There was an error:"
	ERROR_DESC="$(echo $resp | jq '.error_description')"
	echo "$ERROR_DESC"
	if [ "$ERROR_DESC" == '"The request has an invalid grant parameter : code"' ]; then
		echo "Try generating a new auth code - run setup_get_auth_code_url.sh"
	fi
	exit 1
fi

ACCESS_TOKEN=$(echo $resp | jq '.access_token')
ACCESS_TOKEN=${ACCESS_TOKEN//\"/}
REFRESH_TOKEN=$(echo $resp | jq '.refresh_token')
REFRESH_TOKEN=${REFRESH_TOKEN//\"/}

save ACCESS_TOKEN "$ACCESS_TOKEN" "$PARENT/env/auth.py"
save REFRESH_TOKEN "$REFRESH_TOKEN" "$PARENT/env/auth.py"
