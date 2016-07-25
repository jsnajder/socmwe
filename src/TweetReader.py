
import json
import subprocess


def read_tweets(filename, decompress=None, filter_by=None):
    '''
    Reads in tweets. Expects one JSON tweet per line.
    Returns a list of dictionaries.
    '''
    if decompress == 'lzo':
        p = subprocess.Popen(['lzop', '-dc', filename], stdout=subprocess.PIPE)
        for line in p.stdout.readlines():
            tweet = json.loads(line)
            if filter_by is not None and not filter_by(tweet):
                continue
            else:
                yield tweet
        p.wait()
    else:
        with open(filename) as f:
            for line in f:
                tweet = json.loads(line)
                if filter_by is not None and not filter_by(tweet):
                    continue
                else:
                    yield tweet


def tweet_lang(lang):
    return (lambda t: t.get('lang', None) == lang)


def has_field(d, f):
    return d.get(f, None) is not None
