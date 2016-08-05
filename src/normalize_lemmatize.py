
import sys


def load_dict(filename):
    '''Loads a dictionary form file. Each line consists of a word to normalize
       to, and a list of words to normalize from.
    '''
    d = {}
    with open(filename) as f:
        for l in f:
            ws = l.rstrip().split('\t')
            d.update({w: ws[0] for w in ws[1:]})
    return d


def merge_dict(d1, d2):
    z = d1.copy()
    z.update(d2)
    return z


def normalize(d, w, case_insensitive=True, lowercase_output=False):
    '''Normalized the word w using dictionary d. If case_insenstivie=True,
       it will try to match to lowercased or capitalized lexicon entries.
       If lowercase_output=True, it will lowercase the norm after lookup.
    '''
    if w not in d and case_insensitive:
        # Try lowercased
        w2 = w.lower()
        if w2 in d:
            w = w2
        else:
            # Try capitalized
            w2 = w[0].upper() + w[1:].lower()
            if w2 in d:
                w = w2
    norm = d.get(w, w)
    if lowercase_output:
        norm = norm.lower()
    return norm


data = '../data/'
norm1 = data + 'norm-dict-utdallas.txt'
norm2 = data + 'norm-dict-unimelb.txt'
lemma = data + 'lemma-dict.txt'


def main():
    norm_dict = merge_dict(load_dict(norm1), load_dict(norm2))
    lemma_dict = load_dict(lemma)
    filename = sys.argv[1]
    with open(filename) as f:
        for l in f:
            x = l.rstrip().split('\t')
            if len(x) == 1:
                print
                continue
            word = x[0]
            pos = x[1]
            if word[0] == '#' and pos not in '#@~UE$,G' and len(word) > 1:
                word = word[1:]
            norm = normalize(lemma_dict, normalize(norm_dict, word),
                             lowercase_output=True)
            print('\t'.join([x[0], norm, pos]))

if __name__ == "__main__":
    main()
