#!/bin/sh

# ./filter_url.sh tweets.txt

grep -vP '^[^\t]+\t[^t]+\t(#[[:alnum:]]+ )*http://[^ ]+( #[[:alnum:]]+)*$' $1
