#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

config_check=$($DIR/scripts/configure.sh)

if [[ $config_check == "" ]]; then
	$DIR/scripts/build.sh
	$DIR/scripts/flash.sh
	$DIR/scripts/verify.sh
fi
