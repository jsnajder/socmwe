
import sys


def main():
    filename1 = sys.argv[1]  # txt
    filename2 = sys.argv[2]  # conll
    line1 = -1
    line2 = -1
    with open(filename1) as f_txt, open(filename2) as f_conll:
        for l1 in f_txt:
            line1 += 1
            x1 = l1.split('\t')
            t1 = x1[2].strip().decode('utf-8').replace(' ', '').replace(u'\u00a0', '').encode('utf-8')
            t2 = ''
            for l2 in f_conll:
                line2 += 1
                x2 = l2.rstrip().split('\t')
                if len(x2) == 1:
                    break
                t2 += x2[0]
            if t1 != t2:
                print('Mismatch at tweet ID %s, txt line %d, conll line %d:'
                      % (x1[0], line1, line2))
                print('  TXT: "%s"' % t1)
                print('CONLL: "%s"' % t2)
                break


if __name__ == "__main__":
    main()
