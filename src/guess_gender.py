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
    males = read_list('names-male.txt')
    females = read_list('names-female.txt')
    with codecs.open(fname, encoding='utf8') as f:
        for l in f:
            x = l.split('\t')
            userid = x[0]
            names = x[1].split()
            m_names = 0
            f_names = 0
            for n in names:
                if n in males:
                    m_names += 1
                if n in females:
                    f_names += 1
            if m_names == len(names):
                sys.stdout.write('%s\tM\n' % userid)
            elif f_names == len(names):
                sys.stdout.write('%s\tF\n' % userid)


if __name__ == "__main__":
    main()
