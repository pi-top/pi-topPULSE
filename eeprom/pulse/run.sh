#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

while true
do
	read -n1 -r -p "Press f to flash the EEPROM. Press any other key to exit. `echo $'\n> '`" key
	echo ""

	if [ "$key" = 'f' ]; then

		$DIR/scripts/build.sh
		$DIR/scripts/flash.sh
		$DIR/scripts/verify.sh

	else

		exit

	fi
done