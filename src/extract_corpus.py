
import subprocess
import sys


def readlines_lzo(filename):
    p = subprocess.Popen(['lzop', '-dc', filename], stdout=subprocess.PIPE)
    for line in p.stdout.readlines():
        yield line
    p.wait()


ident = 0
lang1 = 4
location = 11
lang2 = 12
text = 13


def country_code(s):
    return s.split('-')[-1] if s != 'None' else None


def main():
    f = sys.argv[1]
    for l in readlines_lzo(f):
        x = l.split('\t')
        lang1 = x[4]
        lang2 = x[12]
        country = country_code(x[11])
        if lang1 == 'en' and lang2 == 'en' and country is not None:
            s = '\t'.join((x[0], country, x[13]))
            sys.stdout.write(s)
        sys.stdout.flush()

if __name__ == "__main__":
    main()
