CLIENT_ID="amzn1.application-oa2-client.bcbbf90ce9474117bb8785cb38cee03e"
CLIENT_SECRET="a686e4e1865b75c52ff36d8ce998fed8ec2771e8ba29e95cffe11a52fa1c3be8"
REDIRECT_URI="https://localhost:9745/authresponse"

DEVICE_TYPE_ID="test_device"

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
