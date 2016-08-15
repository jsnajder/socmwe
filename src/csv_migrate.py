
import csv
import pandas as pd
import sqlite3

cnx = sqlite3.connect('../../data/tweets-db.sqlite')

df = pd.read_csv('../../data/tweet-country-text.txt', 
		 delimiter='\t', encoding='utf-8', index_col=0,
		 quoting=csv.QUOTE_NONE, header=None, 
		 names=['tweet_id', 'country', 'text'])
cnx.execute('CREATE TABLE tweets(tweet_id INT PRIMARY KEY, country STRING, text STRING)')
query=''' insert or replace into tweets (tweet_id,country,text) values (?,?,?) '''
cnx.executemany(query, df.to_records())
cnx.commit()
df = pd.read_csv('../../data/tweet-hashtag.txt', 
		 delimiter='\t', encoding='utf-8', index_col=0,
		 quoting=csv.QUOTE_NONE, header=None, 
		 names=['tweet_id', 'hashtag'])
cnx.execute('CREATE TABLE hashtags(tweet_id INT PRIMARY KEY, hashtag STRING)')
query=''' insert or replace into hashtags (tweet_id,hashtag) values (?,?) '''
cnx.executemany(query, df.to_records())
cnx.commit()

