#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/scripts/build.sh
read
$DIR/scripts/flash.sh
read
$DIR/scripts/verify.sh
