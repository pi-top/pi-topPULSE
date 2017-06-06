#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"

EEPROM_UNIQUE_OUTPUT_FILE="$PARENT/bin/pulse.eep"

echo "Flashing EEPROM..."
sudo $PARENT/tools/eepflash.sh -w -f=$EEPROM_UNIQUE_OUTPUT_FILE -t=24c32
echo "Done."
