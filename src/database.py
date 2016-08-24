
import blaze as bz
#import csv
import unicodecsv as csv
import pandas as pd
import sqlite3
import cPickle
from odo import odo


database_path = '../data/database/'


conn = sqlite3.connect(database_path + 'tweets-db.sqlite')

# tweet_df, user_df, tweet_user_df = pandas_load()

def pandas_pickelize_all():
    pandas_pickelize('tweet', usecols=['tweet_id', 'country']) # NB: Drop tweet text, we don't need it
    pandas_pickelize('user')
    pandas_pickelize('hashtag')
    pandas_pickelize('hashtag-tweet')
    pandas_pickelize('mwe.noNNP', outname='mwe')
    pandas_pickelize('mwe.noNNP-tweet')
    pandas_pickelize('fs')
    pandas_pickelize('fs-tweet')


# Loads a csv into a frame and then pickelizes it
def pandas_pickelize(table, outname=None, usecols=None, quoting=csv.QUOTE_NONE):
    print('Loading %s into a dataframe...' % table)
    if usecols is None:
        table_df = pd.read_csv(database_path + table + '.txt',
                       delimiter='\t', encoding='utf-8', index_col=0, 
                       quoting=quoting)
    else:
        table_df = pd.read_csv(database_path + table + '.txt',
                       delimiter='\t', encoding='utf-8', index_col=0, 
                       usecols=usecols, quoting=quoting)
    print('Pickelizing dataframe...')
    outname = table if outname is None else outname
    with open(database_path + outname + '.pkl', "wb") as f:
        cPickle.dump(table_df, f)


def pandas_depickelize(table):
    print('Loading %s dataframe from a pickle file...' % table)
    with open(database_path + table + '.pkl') as f:
        table_df = cPickle.load(f)
    return table_df


#loads all pickelized dataframes
def pandas_load():
   tweet_df = pandas_depickelize('tweet')
   user_df = pandas_depickelize('user')
   hashtag_df = pandas_depickelize('hashtag')
   mwe_df = pandas_depickelize('mwe.noNNP')
   mwe_tweet_df = pandas_depickelize('mwe.noNNP-tweet')
   return mwe_df, mwe_tweet_df
   

# Reads csv tables into sqlite
# This sets the primary keys
# TODO: Set indices
def sql_migrate():

    df = pd.read_csv(database_path + 'tweet.txt', 
                     delimiter='\t', encoding='utf-8', index_col=0,
                     quoting=csv.QUOTE_MINIMAL,
                     header=0, names=['tweet_id', 'user_id', 'country', 'text']) # required to get a frame of 'objects' dtypes
    sql = """
          CREATE TABLE tweet(
          tweet_id INT PRIMARY KEY, 
          user_id INT NOT NULL UNIQUE, 
          country STRING, 
          text STRING)
          """
    conn.execute(sql)
    query=''' insert or replace into tweet (tweet_id,user_id,country,text) values (?,?,?,?) '''
    conn.executemany(query, df.to_records())
    conn.commit()

#    df = pd.read_csv(database_path + 'tweet-hashtag.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE)
#    conn.execute('CREATE TABLE hashtags(tweet_id INT PRIMARY KEY, hashtag STRING)')
#    query=''' insert or replace into hashtags (tweet_id,hashtag) values (?,?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()

#    df = pd.read_csv(database_path + 'user.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE, 
#                     header=0, names=['user_id', 'gender']) # required to get a frame of 'objects' dtypes
#    conn.execute('CREATE TABLE user(user_id INT PRIMARY KEY, gender STRING)')
#    query = ''' INSERT OR REPLACE INTO user(user_id, gender) values (?, ?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()
    
#    df = pd.read_csv(database_path + 'tweet-user.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE,
#                     header=0, names=['tweet_id', 'user_id']) # required to get a frame of 'objects' dtypes
#    conn.execute('CREATE TABLE tweet_user(tweet_id INT PRIMARY KEY, user_id INT)')
#    query = ''' INSERT OR REPLACE INTO tweet_user(tweet_id, user_id) values (?, ?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()
    
#    df = pd.read_csv(database_path + 'fs.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE)
#    conn.execute('CREATE TABLE fs(fs_id INT PRIMARY KEY, text STRING)')  # TODO: add POS, frequency
#    query = ''' INSERT OR REPLACE INTO fs (fs_id,fs) values (?,?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()
    
#    df = pd.read_csv(database_path + 'fs.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE)
#    conn.execute('CREATE TABLE fs(fs_id INT PRIMARY KEY, text STRING)')  # TODO: add POS, frequency
#    query = ''' INSERT OR REPLACE INTO fs (fs_id,fs) values (?,?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()

#    df = pd.read_csv(database_path + 'fs-tweet.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE)
#    conn.execute('CREATE TABLE fs_tweet(fs_id INT, tweet_id INT)')
#    query = ''' INSERT OR REPLACE INTO fs_tweet(fs_id, tweet_id) values (?, ?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()


def sql_print_tables():
   for table in conn.execute("SELECT name from sqlite_master WHERE type='table';"):
      print(table)
      for key in conn.execute("pragma table_info(%s)" % table):
         print(key)

    
def sql_tweets_with_fs(fs):
    c = conn.execute('SELECT tweet.text FROM fs_tweet INNER JOIN tweet ON tweet.tweet_id = fs_tweet.tweet_id INNER JOIN fs ON fs.fs_id = fs_tweet.fs_id WHERE fs.fs_id = (SELECT fs.fs_id FROM fs WHERE fs.fs = \'%s\')' % fs) 
    for row in c:
        print row

def sql_join_user():
    sql = """
          SELECT tweet.tweet_id, tweet_user.user_id, tweet.country, tweet.text
          FROM tweet INNER JOIN tweet_user ON tweet.tweet_id = tweet_user.tweet_id
          """
    cursor = conn.execute(sql)
    #for r in conn.execute(sql): print r
    with open('tweet3.txt', "wt") as f:
        csv_writer = csv.writer(f, delimiter='\t')
        csv_writer.writerow([x[0] for x in cursor.description])
        csv_writer.writerows(cursor)

#def pandas_
