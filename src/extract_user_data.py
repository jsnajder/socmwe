
import codecs
import sys
import json

def main():
   UTF8Reader = codecs.getreader('utf8')
   sys.stdin = UTF8Reader(sys.stdin)
   for line in sys.stdin:
       try:
           t = json.loads(line)
           if t['lang'] != 'en':
               continue;  
           print(('%s\t%s\t%s' % (t['id'], t['user']['id_str'], t['user']['name'])).encode('utf-8'))
       except:
           continue


if __name__ == "__main__":
    main()

