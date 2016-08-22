import codecs
import sys

def read_list(fname):
    with codecs.open(fname, encoding='utf8') as f:
      s = set()
      for l in f:
          x = l.split()
          s.add(x[0])
    return s


def main():
    fname = sys.argv[1]
    males = 'names-male.txt'
    females = 'names-female.txt'
    with codecs.open(fname) as f:
        for l in f:
            x = l.split('\t')
            userid = x[0]
            names = x[1].split()
            m = 0
            f = 0
            for n in names:
                if n in males:
                    m += 1
                if n in females:
                    f += 1
            if m == len(names):
                sys.stdout.write('%s\tM\n' % userid)
            elif f == len(names):
                sys.stdout.write('%s\tF\n' % userid)


if __name__ == "__main__":
    main()
