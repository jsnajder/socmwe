import cPickle
import codecs
import sys

fi = open('FS_tweet_ids.dat', 'rb')
d = cPickle.load(fi)
fi.close()

fo1 = codecs.open('fsid-fs.txt', 'w', encoding='utf-8')
fo2 = codecs.open('fsid-tweetid.txt', 'w', encoding='utf-8')
for i, (fs, tweetids) in enumerate(d.iteritems()):
    fo1.write('%d\t%s\n' % (i, fs))
    for tweetid in tweetids:
        fo2.write('%d\t%s\n' % (i, tweetid))
fo1.close()
fo2.close()
