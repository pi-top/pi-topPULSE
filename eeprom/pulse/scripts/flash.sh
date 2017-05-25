#!/bin/bash -e

BLANK=0

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"

if [ $BLANK -eq 1 ]; then

	echo "Blanking EEPROM..."
	echo ""
	sudo $PARENT/tools/eepflash.sh -w -f=$PARENT/bin/blank.eep -t=24c32

fi

echo "Flashing EEPROM..."
echo ""
sudo $PARENT/tools/eepflash.sh -w -f=$PARENT/bin/pulse-with-dt.eep -t=24c32
