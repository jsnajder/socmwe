#!/bin/bash

grep -vP '^[^\t]+\t[^t]+\t([^ #]+ ){0,1}(#[[:alnum:]]+ )*http://[^ ]+( #[[:alnum:]]+)*$' $1 | grep -v '#foursquare'
