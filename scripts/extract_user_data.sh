#!/bin/bash

nohup bash -c "lzop -dc /lt/work/arahimi/geotagged/2013/2013.json.lzo | python ../src/extract_user_data.py > ../data/tmp/user-data-2013.txt" &
nohup bash -c "lzop -dc /home/arahimi/datasets/osaka/raw/2014.json.lzo | python ../src/extract_user_data.py > ../data/tmp/user-data-2014.txt" &
nohup bash -c "lzop -dc /home/arahimi/datasets/osaka/raw/2015.json.lzo | python ../src/extract_user_data.py > ../data/tmp/user-data-2015.txt" &

#nohup python ../src/extract_user_data.py /home/arahimi/datasets/osaka/raw/2014.json.lzo > ../data/tmp/user-data-2014.txt &
#nohup python ../src/extract_user_data.py /home/arahimi/datasets/osaka/raw/2015.json.lzo > ../data/tmp/user-data-2015.txt &

