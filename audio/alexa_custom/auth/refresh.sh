#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source "$DIR/env/auth.py"
source "$DIR/env/common.py"

GRANT_TYPE="refresh_token"
resp="$(curl -s -X POST --data "grant_type=${GRANT_TYPE}&refresh_token=${REFRESH_TOKEN}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}&redirect_uri=${REDIRECT_URI}" https://api.amazon.com/auth/o2/token)"

ACCESS_TOKEN=$(echo $resp | jq '.access_token')
ACCESS_TOKEN=${ACCESS_TOKEN//\"/}
REFRESH_TOKEN=$(echo $resp | jq '.refresh_token')
REFRESH_TOKEN=${REFRESH_TOKEN//\"/}

save ACCESS_TOKEN "$ACCESS_TOKEN" "$DIR/env/auth.py"
save REFRESH_TOKEN "$REFRESH_TOKEN" "$DIR/env/auth.py"
