#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"

EEPROM_SETTINGS="$PARENT/src/pulse_eeprom_settings.txt"
EEPROM_BENCHMARK_SETTINGS="$PARENT/src/pulse_eeprom_benchmark_settings.txt"
EEPROM_BLANK_OUTPUT_FILE="$PARENT/bin/blank.eep"
EEPROM_BENCHMARK_OUTPUT_FILE="$PARENT/bin/benchmark.eep"
EEPROM_UNIQUE_OUTPUT_FILE="$PARENT/bin/pulse.eep"

echo "Creating blank eeprom file..."
dd if=/dev/zero ibs=1k count=4 of=$EEPROM_BLANK_OUTPUT_FILE conv=sync
#echo "Use blank image to wipe eeprom"
#sudo $PARENT/tools/eepflash.sh -w -f=$PARENT/bin/blank.eep -t=24c32

echo "Building benchmark .eep for verification..."
$PARENT/tools/eepmake $EEPROM_BENCHMARK_SETTINGS $EEPROM_BENCHMARK_OUTPUT_FILE
truncate --size=4096 $EEPROM_BENCHMARK_OUTPUT_FILE

echo "Building .eep with unique device ID..."
$PARENT/tools/eepmake $EEPROM_SETTINGS $EEPROM_UNIQUE_OUTPUT_FILE

echo "Truncate eep to first 72 bytes (header and vendor ID atom, with CRC)"
truncate --size=72 $EEPROM_UNIQUE_OUTPUT_FILE

echo "Done."
