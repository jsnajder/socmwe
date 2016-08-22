
import blaze as bz
import csv
import pandas as pd
import sqlite3
from odo import odo


database_path = '../data/database/'


conn = sqlite3.connect(database_path + 'tweets-db.sqlite')

# tweet_df, user_df, tweet_user_df = pandas_load()

def pandas_load():
    print 'Loading dataframe tweet...'
    tweet_df = pd.read_csv(database_path + 'tweet.txt',
                   delimiter='\t', encoding='utf-8', index_col=0,
                   quoting=csv.QUOTE_NONE,
                   usecols=['tweet_id', 'country']) # NB: Drop tweet text!
    print 'Loading dataframe user...'
    user_df = pd.read_csv(database_path + 'user.txt',
                  delimiter='\t', encoding='utf-8', index_col=0)
    print 'Loading dataframe tweet-user...'
    tweet_user_df = pd.read_csv(database_path + 'tweet-user.txt',
                        delimiter='\t', encoding='utf-8', index_col=0)
    return tweet_df, user_df, tweet_user_df


# This sets the primary keys
# TODO: Set indices
def sql_migrate():

#    df = pd.read_csv(database_path + 'tweet.txt', 
#                     delimiter='\t', encoding='utf-8', index_col=0,
#                     quoting=csv.QUOTE_NONE)
#    conn.execute('CREATE TABLE tweets(tweet_id INT PRIMARY KEY, country STRING, text STRING)')
#    query=''' insert or replace into tweets (tweet_id,country,text) values (?,?,?) '''
#    conn.executemany(query, df.to_records())
#    conn.commit()

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
    
    df = pd.read_csv(database_path + 'tweet-user.txt', 
                     delimiter='\t', encoding='utf-8', index_col=0,
                     quoting=csv.QUOTE_NONE,
                     header=0, names=['tweet_id', 'user_id']) # required to get a frame of 'objects' dtypes
    conn.execute('CREATE TABLE tweet_user(tweet_id INT PRIMARY KEY, user_id INT)')
    query = ''' INSERT OR REPLACE INTO tweet_user(tweet_id, user_id) values (?, ?) '''
    conn.executemany(query, df.to_records())
    conn.commit()
    
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


def print_tables():
   for table in conn.execute("SELECT name from sqlite_master WHERE type='table';"):
      print(table)
      for key in conn.execute("pragma table_info(%s)" % table):
         print(key)

    
def tweets_with_fs(fs):
    c = conn.execute('SELECT tweet.text FROM fs_tweet INNER JOIN tweet ON tweet.tweet_id = fs_tweet.tweet_id INNER JOIN fs ON fs.fs_id = fs_tweet.fs_id WHERE fs.fs_id = (SELECT fs.fs_id FROM fs WHERE fs.fs = \'%s\')' % fs) 
    for row in c:
        print row

