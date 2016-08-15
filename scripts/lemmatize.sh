#!/bin/bash

# ./lemmatize tweets.filtered.pennpos
# will search for: tweets.filtered.pennpos.conll.{00..07}

data="../data"
lemmatizer="python ../src/normalize_lemmatize.py"

for batch in {00..07}; do
  fi=$1.conll.$batch
  fo=$1.lemmanorm.conll.$batch
  echo "$lemmatizer $fi > $fo"
  nohup $lemmatizer $fi > $fo &
done
