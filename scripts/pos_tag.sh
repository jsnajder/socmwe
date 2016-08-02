#!/bin/sh

data="../../data"
tagger="../../ark-tweet-nlp/ark-tweet-nlp-0.3.2/runTagger.sh"

nohup $tagger --no-confidence --input-format text --output-format conll --input-field 3 $data/tweet-country-text.txt > $data/tweets.pos.txt &
