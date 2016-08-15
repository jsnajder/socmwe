#!/bin/bash

pushd ../../formulaic
nohup python LPR_decomp.py -l en_ark -c ../socmwe/data/tweets.filtered.arkpos.lemmanorm.conll -w 20 -o ../socmwe/data/tweets.filtered.arkpos.lemmanorm.formulaic &
popd
