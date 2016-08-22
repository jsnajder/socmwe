import codecs

def read_list(fname):
    with codecs.open(fname, encoding='utf8') as f:
      s = set()
      for l in f:
          x = l.split()
          if len(x[0]) >= 3:
              s.add(x[0])
    return s


def main():
   m1 = read_list('names-us-census-1990-male.txt')
   m2 = read_list('names-us-ssa-1960-2010-male.txt')
   m3 = read_list('names-wikipedia-male.txt')
   f1 = read_list('names-us-census-1990-female.txt')
   f2 = read_list('names-us-ssa-1960-2010-female.txt')
   f3 = read_list('names-wikipedia-female.txt')
   m0 = m1.union(m2).union(m3)
   f0 = f1.union(f2).union(f3)
   males = m0.difference(f0)
   females = f0.difference(m0)
   f = codecs.open('names-male.txt', 'w', encoding='utf8')
   for name in males:
     f.write('%s\n' % name)
   f.close()
   f = codecs.open('names-female.txt', 'w', encoding='utf8')
   for name in females:
     f.write('%s\n' % name)
   f.close()


if __name__ == "__main__":
    main()
