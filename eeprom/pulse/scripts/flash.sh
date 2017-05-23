#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"

echo "Blanking EEPROM..."
echo ""
sudo $PARENT/tools/eepflash.sh -w -f=$PARENT/bin/blank.eep -t=24c32
echo "Flashing EEPROM..."
echo ""
sudo $PARENT/tools/eepflash.sh -w -f=$PARENT/bin/pulse-with-dt.eep -t=24c32
