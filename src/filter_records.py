import sys
import codecs

# Filters lines from f2 for which the key exists in f1. In both files, the key is the first field.

def main():
    f1_name = sys.argv[1]
    f2_name = sys.argv[2]
    f = codecs.open(f1_name, encoding='utf8')
    tweets = set()
    for l in f:
        xs = l.split('\t')  
        tweets.add(xs[0])
    f.close()
    f = codecs.open(f2_name, encoding='utf8')
    for l in f:
        xs = l.split('\t')
        if xs[0] in tweets:
            sys.stdout.write(l.encode('utf8'))
    f.close()
    
if __name__ == "__main__":
    main()
