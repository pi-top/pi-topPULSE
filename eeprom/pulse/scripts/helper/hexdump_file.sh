#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"
ROOT="$(dirname $PARENT)"

xxd $ROOT/bin/pulse-with-dt.eep
