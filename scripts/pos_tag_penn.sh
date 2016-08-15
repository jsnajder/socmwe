#!/bin/bash

data="../data"
tagger="../../ark-tweet-nlp/ark-tweet-nlp-0.3.2/runTagger.sh"
model="../../ark-tweet-nlp/penn-model/model.ritter_ptb_alldata_fixed.20130723"

for batch in {00..07}; do
  nohup $tagger --model $model --no-confidence --input-format text --output-format conll --input-field 3 $data/tweets.filtered.txt.$batch > $data/tweets.filtered.pennpos.conll.$batch &
done
