#!/bin/bash

CONFIG="/boot/config.txt"
EEPROM_I2C="/dev/i2c-0"

if [ ! -e $EEPROM_I2C ]; then
	if [ -e $CONFIG ] && grep -q "^dtparam=i2c_vc=on$" $CONFIG; then
		:
	else
		echo "dtparam=i2c_vc=on" | sudo tee -a $CONFIG &> /dev/null
	fi
	echo "YOU NEED TO REBOOT"
fi
