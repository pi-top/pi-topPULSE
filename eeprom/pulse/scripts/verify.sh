#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

diff -y <($DIR/helper/hexdump_file.sh) <($DIR/helper/hexdump_device.sh) | head -n 50 | $DIR/../tools/colordiff
