
import codecs
import sys


def main():
    filename1 = sys.argv[1]  # txt
    filename2 = sys.argv[2]  # conll
    line1 = -1
    line2 = -1
    with open(filename1) as f_txt, \
         open(filename2) as f_conll:
        for l1 in f_txt:
            line1 += 1
            x1 = l1.split('\t')
            print x1[0]
            for l2 in f_conll:
                line2 += 1
	        if l2 == '\n':
	            break
                sys.stdout.write(l2)


if __name__ == "__main__":
    main()
