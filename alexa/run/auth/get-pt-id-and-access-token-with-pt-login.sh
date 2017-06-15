#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source $DIR/config

PT_USERNAME="${1:-$PT_USERNAME}"

if [[ "$PT_USERNAME" == "" ]]; then
	printf "Enter your pi-top account username: "
	read PT_USERNAME
	printf "\n"
	export PT_USERNAME
fi

stty -echo
printf "Enter your pi-top account password: "
read PT_PASSWORD
stty echo
printf "\n"

resp=$(curl -s -XPOST -H "Content-Type: application/json" -d "{
    \"username\": \"$PT_USERNAME\",
    \"password\": \"$PT_PASSWORD\"
}" "$PT_API_URL/Accounts/login")

USER_ID=$(echo "$resp" | jq .userId -r)
ACCESS_TOKEN=$(echo "$resp" | jq .id -r)

if [[ $USER_ID != "null" ]] && [[ $ACCESS_TOKEN != "null" ]]; then
	echo "USER ID: $USER_ID"
	echo "ACCESS TOKEN: $ACCESS_TOKEN"
else
	echo "Unable to get pi-top account user ID and access token - are you sure your credentials are correct?"
	exit 1
fi
