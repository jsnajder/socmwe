import sys
import codecs

# Reads in a file with ids and values on each row (tab separated), and generates two files: list of id-values and a join list which linkes the two ids

def main():

    fname = sys.argv[1]
    f = codecs.open(fname, encoding='utf8')
    d = {}
    for l in f:
        xs = l.split('\t')  
        index = xs[0]
        value = xs[1]
        if value not in d:
            d[value] = []
        d[value].append(index)
    f.close()   
 
    fo1 = codecs.open('value.txt', 'w', encoding='utf-8')
    fo2 = codecs.open('value-index.txt', 'w', encoding='utf-8')

    for j, (value, index) in enumerate(d.iteritems()):
       fo1.write('%s\t%s\n' % (j, value))
       for i in index:
           fo2.write('%s\t%s\n' % (j, i))

    fo1.close()
    fo2.close()
   
 
if __name__ == "__main__":
    main()
