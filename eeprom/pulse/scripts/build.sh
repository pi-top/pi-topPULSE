#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"

echo "Building device tree overlay..."
sudo dtc -@ -I dts -O dtb -o $PARENT/bin/pulse.dtb $PARENT/src/pulse.dts
echo "chown pi"
sudo chown pi:pi $PARENT/bin/pulse.dtb
echo "Building .eep with device tree..."
echo ""
$PARENT/tools/eepmake $PARENT/src/pulse_eeprom_settings.txt $PARENT/bin/pulse-with-dt.eep $PARENT/bin/pulse.dtb # -c myparams.json
