
from multiprocessing import Pool
from os import listdir
from os.path import join, basename
import sys
from TweetReader import read_tweets, has_field, tweet_lang


def check_tweets(tweets_gen):
    tweets = 0
    tweet_coordinates = 0
    tweet_place = 0
    user_location = 0
    for t in tweets_gen:
        tweets += 1
        if has_field(t, 'coordinates'):
            tweet_coordinates += 1
        if has_field(t, 'place'):
            tweet_place += 1
        if has_field(t['user'], 'location'):
            user_location += 1
    return {'tweets': tweets,
            'tweet_coordinates': tweet_coordinates,
            'tweet_place': tweet_place,
            'user_location': user_location}


def read_and_check(f):
    ts = read_tweets(f, decompress='lzo',
                     filter_by=tweet_lang('en'))
    c = check_tweets(ts)
    print('%s: %s' % (basename(f), c))
    return c


def dict_add(d1, d2):
    return {x: d1.get(x, 0) + d2.get(x, 0) for x in set(d1).union(d2)}


def main():
    path = sys.argv[1]
    fs = [join(path, f) for f in listdir(path) if f.endswith('lzo')]
    p = Pool(5)
    cs = p.map(read_and_check, fs)
    p.close()
    p.join()
    print 'TOTAL:'
    print cs
    total = reduce(dict_add, cs)
    print total


if __name__ == "__main__":
    main()
