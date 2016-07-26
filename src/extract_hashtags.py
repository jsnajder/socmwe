
import re
import sys

hashtag_re = re.compile('#\w+')


def main():
    filename = sys.argv[1]
    with open(filename) as f:
        for l in f:
            x = l.split('\t')
            for h in hashtag_re.findall(x[2]):
                s = '\t'.join((x[0], h))
                print s


if __name__ == "__main__":
    main()
