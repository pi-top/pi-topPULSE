#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"
ROOT="$(dirname $PARENT)"

TEMP_FILE=/tmp/eeprom_test_file
TEMP_DEVICE=/tmp/eeprom_test_device

source $ROOT/py/config.py

echo "Comparing eeprom data on device with benchmark eeprom file..."

cp $PARENT/bin/benchmark.eep $TEMP_FILE
sudo cp /sys/class/i2c-adapter/i2c-0/0-0050/eeprom $TEMP_DEVICE
sudo chown pi:pi $TEMP_DEVICE

# Overwrite the first 72 bytes for the comparison, as we expect these to be different
dd conv=notrunc if=/dev/zero of=$TEMP_FILE bs=1 count=72 &> /dev/null
dd conv=notrunc if=/dev/zero of=$TEMP_DEVICE bs=1 count=72 &> /dev/null

cmp $TEMP_FILE $TEMP_DEVICE

if [ "$?" != 0 ]; then

	echo -e "\033[0;31mWARNING: A difference was detected between the benchmark and eeprom data (beyond the 72 byte header)\033[0m"
	echo "Showing full diff:"
	$PARENT/tools/colordiff -y --width=138 <($DIR/helper/hexdump_file.sh) <($DIR/helper/hexdump_device.sh)

elif [ $EEPROM_VERIFY_LINES_TO_SHOW -gt 0 ]; then

	echo -e "\033[0;32mNo differences found outside of first 72 byte header. Showing comparison of header:\033[0m"
	diffResp=$($PARENT/tools/colordiff -y --width=138 <($DIR/helper/hexdump_file.sh) <($DIR/helper/hexdump_device.sh))
	echo "$diffResp" | head -n $EEPROM_VERIFY_LINES_TO_SHOW

fi

