#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/config

PT_USER_ID="${1:-$PT_USER_ID}"
PT_ACCESS_TOKEN="${2:-$PT_ACCESS_TOKEN}"

if [[ "$PT_USER_ID" == "" ]]; then
	echo "Usage: <script> <pi-top user ID> <pi-top access token>"
	exit
fi

if [[ "$PT_ACCESS_TOKEN" == "" ]]; then
	echo "Usage: <script> <pi-top user ID> <pi-top access token>"
	exit
fi

ROUTE="$PT_API_URL/Accounts/$PT_USER_ID/AVSAccessToken"

cmd="curl -s $ROUTE?access_token=$PT_ACCESS_TOKEN"

AVS_ACCESS_TOKEN="$($cmd | jq .data.access_token -r)"

if [[ "$AVS_ACCESS_TOKEN" != "null" ]]; then
	echo "$AVS_ACCESS_TOKEN"
	exit 0
else
	exit 1
fi