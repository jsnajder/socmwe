import codecs

def read_conll_mwetagged_tweet(corpus_path, start=0, stop=-1, corpus_encoding='utf-8'):
    '''
    CONLL+tweetId reader.
    CONLL = token_id, word, lemma, pos, mwe_tag, parent_offset, strenth, ...
    '''
    f = codecs.open(corpus_path,encoding=corpus_encoding)
    sentence = []
    sentence_count = -1
    for line in f:
        x = line.rstrip().split('\t')
        if len(x) == 1:
            if sentence_count >= 0 and start <= sentence_count:
                yield (tweet_id, sentence)
            tweet_id = x[0]
            sentence = []
            sentence_count += 1
            if sentence_count == stop:
                break
        else:
            try:
               ws = line.strip().split("\t")
     	       lemma = ws[2]
               mwe_tag = ws[4]
               strength = ws[6]
               sentence.append([lemma, mwe_tag, strength])
            except:
              continue
    if sentence_count < stop: 
      yield (tweet_id, sentence)

data_path = '../data/'
fi = data_path + 'tweets.filtered.pennpos.mwe.conll-tweetid'

def extract_mwes(tokens):
    n = len(tokens)
    mwes = []
    for i in range(0, n):
        print i
        if tokens[i][1][0] == 'B':
            j = i
            mwe = [tokens[j][0]]
            j += 1
            while j < n and (tokens[j][2] == "_" or tokens[j][2] == "~"):
                print j, tokens[j][2], tokens[j][0]
                mwe.append(tokens[j][0])
                j += 1
            if len(mwe) > 1: 
                mwes.append(mwe)
    yield mwes
               

