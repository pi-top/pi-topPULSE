#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

"$DIR/helper/setup_get_auth_code_url.sh"
"$DIR/helper/setup_get_auth_and_refresh_tokens.sh"
