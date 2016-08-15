#!/bin/bash

# ./conll_merge.sh tweets.filtered.pennpos.conll > tmp.txt
# merges conll files, after REMOVING LAST LINE from each conll file (ARK tagger's summary)

for batch in {00..07}; do
  head -n -1 $1.$batch
done
