#!/bin/bash -e

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

if [ -f "$DIR/common.py" ]; then
	source "$DIR/common.py"
else
	echo "No 'common' file"
	exit 1
fi

function urlencode() {
	perl -MURI::Escape -ne 'chomp;print uri_escape($_),"\n"'
}
export -f urlencode

function save() {
	key="$1"
	value="$2"
	file="$3"
	if [ -f $file ] && grep -q $key= $file; then
		sed -i "s/$key=.*/$key=\"$value\"/1" $file
	else
		echo "$key=\"$value\"" >> $file
	fi
}
export -f save
