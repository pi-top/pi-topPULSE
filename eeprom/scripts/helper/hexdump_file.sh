#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PARENT="$(dirname $DIR)"
ROOT="$(dirname $PARENT)"

EEPROM_BENCHMARK_OUTPUT_FILE="$ROOT/bin/benchmark.eep"

xxd $EEPROM_BENCHMARK_OUTPUT_FILE
