# -*- coding: utf-8 -*-
"""
Created on Tue Oct 01 16:06:07 2019

@author: Adarsh
"""
import re
import tweepy #https://github.com/tweepy/tweepy
from wordcloud import WordCloud
import matplotlib.pyplot as plt
#Twitter API credentials
consumer_key = "Kq4mCtnOSPiNwA9ArvYq03DE7"
consumer_secret = "aWBfVbrJWppmEy3mAbrjUHa6Y8AKU6qkCBZwA6ZpAO8BEFaoC2"
access_key = "529590041-eZXHHkluorWkdRZRWiVYW3GVBuvr3VXt84cZcDYA"
access_secret = "rqlG8jzmKTPU3bZoCwgRnOUoD5UYOx8KDjhoXySPrR3mI"


def get_all_tweets(screen_name):
    auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    alltweets = []	
    new_tweets = api.user_timeline(screen_name = screen_name,count=200)
    alltweets.extend(new_tweets)
    
    oldest = alltweets[-1].id - 1
    while len(new_tweets)>0:
        new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
        #save most recent tweets
        alltweets.extend(new_tweets)
        #update the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1
        print ("...%s tweets downloaded so far" % (len(alltweets)))                # tweet.get('user', {}).get('location', {})
 
    outtweets = [[tweet.created_at,tweet.entities["hashtags"],tweet.entities["user_mentions"],tweet.favorite_count,
                  tweet.geo,tweet.id_str,tweet.lang,tweet.place,tweet.retweet_count,tweet.retweeted,tweet.source,tweet.text,
                  tweet._json["user"]["location"],tweet._json["user"]["name"],tweet._json["user"]["time_zone"],
                  tweet._json["user"]["utc_offset"]] for tweet in alltweets]
    
    import pandas as pd
    tweets_df = pd.DataFrame(columns = ["time","hashtags","user_mentions","favorite_count",
                                    "geo","id_str","lang","place","retweet_count","retweeted","source",
                                    "text","location","name","time_zone","utc_offset"])
    tweets_df["time"]  = pd.Series([str(i[0]) for i in outtweets])
    tweets_df["hashtags"] = pd.Series([str(i[1]) for i in outtweets])
    tweets_df["user_mentions"] = pd.Series([str(i[2]) for i in outtweets])
    tweets_df["favorite_count"] = pd.Series([str(i[3]) for i in outtweets])
    tweets_df["geo"] = pd.Series([str(i[4]) for i in outtweets])
    tweets_df["id_str"] = pd.Series([str(i[5]) for i in outtweets])
    tweets_df["lang"] = pd.Series([str(i[6]) for i in outtweets])
    tweets_df["place"] = pd.Series([str(i[7]) for i in outtweets])
    tweets_df["retweet_count"] = pd.Series([str(i[8]) for i in outtweets])
    tweets_df["retweeted"] = pd.Series([str(i[9]) for i in outtweets])
    tweets_df["source"] = pd.Series([str(i[10]) for i in outtweets])
    tweets_df["text"] = pd.Series([str(i[11]) for i in outtweets])
    tweets_df["location"] = pd.Series([str(i[12]) for i in outtweets])
    tweets_df["name"] = pd.Series([str(i[13]) for i in outtweets])
    tweets_df["time_zone"] = pd.Series([str(i[14]) for i in outtweets])
    tweets_df["utc_offset"] = pd.Series([str(i[15]) for i in outtweets])
    tweets_df.to_csv(screen_name+"_tweets.csv")
    return tweets_df

I_srk = get_all_tweets("iamsrk")

#cadd_centre_tweets = get_all_tweets("DreamZoneSchool")
		
text=I_srk.text
import re

ip_rev_string = " ".join(text)

ip_rev_string = re.sub("[^A-Za-z" "]+"," ",ip_rev_string).lower()
ip_rev_string = re.sub("[0-9" "]+"," ",ip_rev_string)

ip_reviews_words = ip_rev_string.split(" ")

#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer=TfidfVectorizer(ip_reviews_words,use_idf=True,ngram_range=(1, 3))
X=vectorizer.fit_transform(ip_reviews_words)

#stop words
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
stop_words = stopwords.words('english')
stopwordss=[w for w in ip_reviews_words if not w in stop_words]

#stemming
from nltk.stem import PorterStemmer
ps=PorterStemmer()
stemm=[]
for w in stopwordss:
    stemm.append(ps.stem(w))
    
# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(stemm)


wordcloud_ip = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_rev_string)
plt.imshow(wordcloud_ip)


#creating positive words
with open("E:/ADM/Excelr solutions/DS assignments/Text mining/positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")

posword=poswords[36:]

with open("E:/ADM/Excelr solutions/DS assignments/Text mining/negative-words.txt","r") as neg:
  negwords = neg.read().split("\n")

negwords = negwords[37:]

# negative word cloud
# Choosing the only words which are present in negwords
ip_neg_in_neg = " ".join ([w for w in ip_reviews_words if w in negwords])

wordcloud_neg_in_neg = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_neg_in_neg)

plt.imshow(wordcloud_neg_in_neg)

# Positive word cloud
# Choosing the only words which are present in positive words
ip_pos_in_pos = " ".join ([w for w in ip_reviews_words if w in poswords])
wordcloud_pos_in_pos = WordCloud(
                      background_color='white',
                      width=1800,
                      height=1400
                     ).generate(ip_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)


#########
from textblob import TextBlob
text=I_srk.text

ip_pos_in_pos
blob=TextBlob(ip_neg_in_neg)
print(blob.sentiment)


#storing negative polarity and subjectivity
nltk.download('punkt')
negblob=blob.sentiment
t=(blob.polarity)
for s in blob.sentences:
    if s.polarity < -0.2:
        print(s)
        
        
print(blob.sentences)
import requests

blob.polarity #0.39
blob.sentences

# writng reviews in a text file 
with open("pos.txt","w",encoding='utf8') as output:
    output.write(str(ip_pos_in_pos))

import os
os.getcwd()

text1 = open("pos.txt")
text1=text1.read()

ip_pos_in_pos
blob2=TextBlob(ip_pos_in_pos)

#here you will get polarity and subjectivity,how positive you get the information and subjectivity means how factual (or) opinion the data.
print(blob2.sentiment)
blob2.polarity #0.57






