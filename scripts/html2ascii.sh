#!/bin/bash

sed -e 's/\&amp;/\&/g' -e 's/\&gt;/>/g' -e 's/\&lt;/</g' $1
