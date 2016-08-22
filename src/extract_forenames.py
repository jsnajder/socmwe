import sys
import codecs

def main():
    fname = sys.argv[1]
    f = codecs.open(fname, encoding='utf8')
    d = {}
    for line in f:
       try:
           xs = line.split('\t')
           userid = xs[1]
           names = [s for s in xs[2].rstrip().split() if s.isalpha()]
           if len(names) <= 1 or len(names[0]) < 3:
             continue
           if userid not in d:
               d[userid] = set()
           d[userid].add(names[0].lower())
       except:
           continue
    for userid, forenames in d.iteritems():
        sys.stdout.write(('%s\t%s\n' % (userid, ' '.join(forenames))).encode('utf-8'))
#        sys.stdout.write(('%s\t%s\n' % (userid, forenames)).encode('utf-8'))

if __name__ == "__main__":
    main()
