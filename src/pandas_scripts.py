
import blaze as bz
import csv
import pandas as pd
import sqlite3
from odo import odo

data_path = '../data/'

cnx = sqlite3.connect('../data/tweets-db.sqlite')

def csv_sql():
	'''CSV to SQLite vs Pandas dataframe'''
	'''(I could have used the "into" package instead.)'''
	tweets_df = pd.read_csv('../../data/tweet-country-text.1000.txt', 
				delimiter='\t', 
				encoding='utf-8',
				index_col=0,
				quoting=csv.QUOTE_NONE, header=None, 
				names=['tweet_id', 'country', 'text'])
	tweets_df.to_sql('tweets', cnx)

# tweets_db = bz.Data('sqlite:///../data/tweets-1000-db.sqlite::tweets')


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

def join_hashtags():
	dfs = []
	for lang in ['us', 'gb', 'id', 'ca', 'ph', 'au', 'in']:
	 	dfs.append(pd.read_csv('../../data/hashtags.%s.txt' % lang, index_col=0, 
     				       nrows=100, names=['hashtag', lang]))
	return pd.concat(dfs, axis=1).fillna(0)

langs = ['us', 'gb', 'ca', 'au']

def hashtags():
	df = pd.read_csv('../../data/country-hashtag.lowercased.txt', delimiter='\t', header=None, names=['country', 'hashtag'])
	dfs = []
	for lang in langs:
		s = df[df['country'] == lang]['hashtag'].value_counts().rename(lang)
		s.index.name = 'hashtag'
		dfs.append(s)
	return pd.concat(dfs, axis=1).fillna(0).astype('int32').set_index('hashtag')

hashtags_df = pd.read_csv(data_path + 'hashtags.csv', index_col=0)

#probs:
hashtag_probs_df =  hashtags_df.loc[:,'us':'au'].div(hashtags_df.sum(axis=0), axis=1)

def above_threshold(df, t):
	return df[(df['us'] + df['ca'] > t) & (df['gb'] > t) & (df['au'] > t)]

#df['us'].rank(ascending=False).astype('int').sort_values(ascending=True)

#above_threshold(500).sum(axis=1).sort_values(ascending=False)

