#!/bin/sh

data="../data"
tagger="../../ark-tweet-nlp/ark-tweet-nlp-0.3.2/runTagger.sh"

for batch in {00..03}; do
  nohup $tagger --no-confidence --input-format text --output-format conll --input-field 3 $data/tweets.filtered.txt.$batch > $data/tweets.pos.txt.$batch &
done
