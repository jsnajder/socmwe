import codecs
import sys
import cPickle

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
     	       pos = ws[3]
               mwe_tag = ws[4]
               sentence.append([lemma, mwe_tag, pos])
            except:
              continue
    if sentence_count < stop: 
      yield (tweet_id, sentence)

#data_path = '../data/tweets-processed/'
#fi = data_path + 'tweets.filtered.pennpos.mwe.conll-tweetid'
fi = '../data/tmp/mwe-test.conll'

i_strong = u'\u012A'
i_weak   = u'\u0128'
i_strong_gap = u'\u012B'
i_weak_gap = u'\u0129'

def extract_mwes(tokens):
    n = len(tokens)
    mwes = []
    for i in range(0, n):
        mwe_weak = []
        mwe_strong = []
        if tokens[i][1][0] == 'B' or (i+1 < n and tokens[i][1][0] == i_weak and tokens[i+1][1][0] == i_strong):
            mwe_strong = extract_strong_gappy(tokens, i)
        if tokens[i][1][0] == 'B':
            mwe_weak = extract_weak_gappy(tokens, i)
	if tokens[i][1][0] == 'b':
            mwe_strong = extract_strong_gapfilling(tokens, i)
            mwe_weak = extract_weak_gapfilling(tokens, i)
        if len(mwe_strong) > 1: 
            mwes.append((mwe_strong, 'S'))
        if len(mwe_weak) > 1: 
            mwes.append((mwe_weak, 'W'))
    return mwes
               
def extract_strong_gappy(tokens, i):
    n = len(tokens)
    j = i
    mwe = [(tokens[j][0], tokens[j][2])]
    j += 1
    last_is_strong = False
    while j < n and (tokens[j][1][0] == i_strong or tokens[j][1][0].islower()):
        if tokens[j][1][0] == i_strong:
           last_is_strong = True
        else:
           last_is_strong = False 
        if tokens[j][1][0].islower():
            word = '*'
            pos = '*'
            while j < n and tokens[j][1][0].islower():
               j += 1
        else:
            word = tokens[j][0]
            pos = tokens[j][2]
            j += 1
        mwe.append((word, pos))
    return mwe if last_is_strong else []

def extract_strong_gapfilling(tokens, i):
    n = len(tokens)
    j = i
    mwe = [(tokens[j][0], tokens[j][2])]
    j += 1
    while j < n and (tokens[j][1][0] == i_strong_gap):
        word = tokens[j][0]
        pos = tokens[j][2]
        mwe.append((word, pos))
        j += 1
    return mwe

def extract_weak_gappy(tokens, i):
    n = len(tokens)
    j = i
    mwe = [(tokens[j][0], tokens[j][2])]
    j += 1
    seen_weak = False
    while j < n and (tokens[j][1][0] == i_strong or tokens[j][1][0] == i_weak or tokens[j][1][0].islower()):
        if tokens[j][1][0] == i_weak:
            seen_weak = True
        if tokens[j][1][0].islower():
            word = '*'
            pos = '*'
            while j < n and tokens[j][1][0].islower():
               j += 1
        else:
            word = tokens[j][0]
            pos = tokens[j][2]
            j += 1
        mwe.append((word, pos))
    if not seen_weak:
	return []
    else:
        return mwe

def extract_weak_gapfilling(tokens, i):
    n = len(tokens)
    j = i
    mwe = [(tokens[j][0], tokens[j][2])]
    j += 1
    while j < n and (tokens[j][1][0] == i_weak_gap):
        word = tokens[j][0]
        pos = tokens[j][2]
        mwe.append((word, pos))
        j += 1
    return mwe

def most_common(l):
    return max(set(l), key=l.count)

def main():

    if len(sys.argv) != 2:
        print('Usage: mweconll2index.py <mwe.conll-tweetid file>')
        sys.exit(0)

    fi = read_conll_mwetagged_tweet(sys.argv[1])
    d_mwe = {}

    for j, (tweetid, tokens) in enumerate(fi):
        try:
          for mwe_pos, typ in extract_mwes(tokens):
              mwe, pos = zip(*mwe_pos)
              mwe_string = ' '.join(mwe)
              pos_string = ' '.join(pos)
              if mwe_string not in d_mwe:
                 d_mwe[mwe_string] = {'tweetid' : [], 'pos' : [], 'type' : []}
              d_mwe[mwe_string]['tweetid'].append(tweetid)
              d_mwe[mwe_string]['pos'].append(pos_string)
              d_mwe[mwe_string]['type'].append(typ)
              #sys.stdout.write(('%s\t%s\t%s\t%s\n' % (tweetid, typ, mwe_string, pos_string)).encode('utf-8'))
        except:
          print('error:')
          print j, tweetid, tokens
	if j % 1000000 == 0:
          print('%d tweets processed' % j)

#    print d_mwe

    fo1 = codecs.open('mwe.txt', 'w', encoding='utf-8')
    fo2 = codecs.open('mwe-tweet.txt', 'w', encoding='utf-8')

    for i, (mwe, x) in enumerate(d_mwe.iteritems()):
        freq = len(x['tweetid'])
        pos = most_common(x['pos'])
        typ = most_common(x['type'])
        fo1.write(u'%d\t%s\t%s\t%s\t%d\n' % (i, mwe, pos, typ, freq))
        for tweetid in x['tweetid']:
            fo2.write(u'%d\t%s\n' % (i, tweetid))

    fo1.close()
    fo2.close()

if __name__ == "__main__":
    main()
   
