
import sys
from TweetReader import read_tweets

def main():
    f = sys.argv[1]
    tweets = read_tweets(f, decompress='lzop', filter_by=lambda t: t['lang']=='en')
    for t in tweets:
        print(('%s\t%s\t%s' % (t['id'], t['user']['id_str'], t['user']['name'])).encode('utf-8'))

if __name__ == "__main__":
    main()

