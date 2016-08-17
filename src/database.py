
import blaze as bz
import csv
import pandas as pd
import sqlite3
from odo import odo

database_path = '../data/database/'

conn = sqlite3.connect(database_path + 'tweets-db.sqlite')

def print_tables():
   for table in conn.execute("SELECT name from sqlite_master WHERE type='table';"):
      print(table)
      for key in conn.execute("pragma table_info(%s)" % table):
         print(key)
    
#def create_tables():
#    conn.execute('CREATE TABLE mwe(mwe_id INT PRIMARY KEY, method INT, mwe STRING)')

def import_fs():
    df = pd.read_csv(database_path + 'fsid-fs.txt', 
                     delimiter='\t', encoding='utf-8', index_col=0,
                     quoting=csv.QUOTE_NONE, header=None, 
                     names=['fs_id', 'fs'])
    conn.execute('CREATE TABLE fs(fs_id INT PRIMARY KEY, fs STRING)')
    query = ''' INSERT OR REPLACE INTO fs (fs_id,fs) values (?,?) '''
    conn.executemany(query, df.to_records())
    conn.commit()
    df = pd.read_csv(database_path + 'fsid-tweetid.txt', 
                     delimiter='\t', encoding='utf-8', index_col=0,
                     quoting=csv.QUOTE_NONE, header=None, 
                     names=['fs_id', 'tweet_id'])
    conn.execute('CREATE TABLE fs_tweet(fs_id INT, tweet_id INT)')
    query = ''' INSERT OR REPLACE INTO fs_tweet(fs_id, tweet_id) values (?, ?) '''
    conn.executemany(query, df.to_records())
    conn.commit()
   
def tweets_with_fs(fs):
    c = conn.execute('SELECT tweet.text FROM fs_tweet INNER JOIN tweet ON tweet.tweet_id = fs_tweet.tweet_id INNER JOIN fs ON fs.fs_id = fs_tweet.fs_id WHERE fs.fs_id = (SELECT fs.fs_id FROM fs WHERE fs.fs = \'%s\')' % fs) 
    for row in c:
      print row

# This uses tweet_id as the primary key
def migrate_sql():

	df = pd.read_csv('../data/tweets.filtered.txt', 
			 delimiter='\t', encoding='utf-8', index_col=0,
			 quoting=csv.QUOTE_NONE, header=None, 
			 names=['tweet_id', 'country', 'text'])
	cnx.execute('CREATE TABLE tweets(tweet_id INT PRIMARY KEY, country STRING, text STRING)')
	query=''' insert or replace into tweets (tweet_id,country,text) values (?,?,?) '''
	cnx.executemany(query, df.to_records())
	cnx.commit()

	df = pd.read_csv('../data/tweet-hashtag.txt', 
			 delimiter='\t', encoding='utf-8', index_col=0,
			 quoting=csv.QUOTE_NONE, header=None, 
			 names=['tweet_id', 'hashtag'])
	cnx.execute('CREATE TABLE hashtags(tweet_id INT PRIMARY KEY, hashtag STRING)')
	query=''' insert or replace into hashtags (tweet_id,hashtag) values (?,?) '''
	cnx.executemany(query, df.to_records())
	cnx.commit()


