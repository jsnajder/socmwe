
import json
import subprocess


def read_tweets(filename, decompress=None, filter=None):
    '''
    Reads in tweets. Expects one JSON tweet per line.
    Returns a list of dictionaries.
    '''
    if decompress == 'lzo':
        p = subprocess.Popen(['lzop', '-dc', filename], stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            tweet = json.loads(line)
            if filter is not None and not filter(tweet):
                continue
            else:
                yield tweet
        p.wait()
    else:
        with open(filename) as f:
            for line in f:
                tweet = json.loads(line)
                if filter is not None and not filter(tweet):
                    continue
                else:
                    yield tweet


def filter_lang(lang):
    return (lambda tweet: tweet.get('lang', None) == lang)