
import codecs
import sys
import re
import htmlentitydefs
import unicodedata


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

##
# Removes HTML or XML character references and entities from a text string.
#
# @param text The HTML (or XML) source text.
# @return The plain text, as a Unicode string, if necessary.


def unescape(text):
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text  # leave as is
    return re.sub("&#?\w+;", fixup, text)


def main():
    filename1 = sys.argv[1]  # txt
    filename2 = sys.argv[2]  # conll
    line1 = -1
    line2 = -1
    with open(filename1) as f_txt, \
         open(filename2) as f_conll:
#    with codecs.open(filename1, encoding='utf-8') as f_txt, \
#         codecs.open(filename2, encoding='utf-8') as f_conll:
        for l1 in f_txt:
            line1 += 1
	    l1 = l1.decode('utf-8')
            x1 = l1.split('\t')
            t1 = x1[2].strip().replace(' ', '').\
                 replace(u'\u00a0', '').replace(u'\u200a', '').replace(u'\u3000', '').\
                 replace(u'\u2002', '').replace(u'\u2003', '').replace(u'\u2004', '').\
                 replace(u'\u2005', '').replace(u'\u2006', '').replace(u'\u2007', '').\
                 replace(u'\u2008', '').replace(u'\u2009', '').replace(u'\u200B', '').\
                 replace(u'&amp;gt;', '>').replace(u'&amp;lt;', '<').replace(u'&nbsp;', '').\
		 replace(u'&amp;amp;', '&')
            t1 = unescape(t1)  # unescape must come first, as it can introduce control characters
            t1 = remove_control_characters(t1)
            t2 = ''
            for l2 in f_conll:
                line2 += 1
                l2 = l2.decode('utf-8')
	        if l2 == '\n':
	            break
                x2 = l2.rstrip().split('\t')
                t2 += remove_control_characters(x2[0])
            if t1 != t2:
                print('Mismatch at tweet ID %s, txt line %d, conll line %d:'
                      % (x1[0], line1, line2))
		print l1
                print('  TXT: "%s"' % t1)
                print('CONLL: "%s"' % t2)
                break


if __name__ == "__main__":
    main()
