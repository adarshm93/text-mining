# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 11:29:34 2019

@author: Adarsh
"""

################# IMDB reviews extraction ######################
from selenium import webdriver
browser = webdriver.Chrome() # opens the chrome browser
from bs4 import BeautifulSoup as bs

## Moana Movie #####
page= "http://www.imdb.com/title/tt3521164/reviews?ref_=tt_urv"
# Importing few exceptions to surpass the error messages while extracting reviews 
from selenium.common.exceptions import NoSuchElementException 
from selenium.common.exceptions import ElementNotVisibleException


browser.get(page)
import time
reviews = []
i=1
# Below while loop is to load all the reviews into the browser till load more button dissapears
while (i>0):
    #i=i+25
    try:
        # Storing the load more button page xpath which we will be using it for click it through selenium 
        # for loading few more reviews
        button = browser.find_element_by_xpath('.collapsable+ .collapsable .show-more__control') # //*[@id="load-more-trigger"]
        button.click()
        time.sleep(5)
    except NoSuchElementException:
        break
    except ElementNotVisibleException:
        break

# Getting the page source for the entire imdb after loading all the reviews
ps = browser.page_source 
#Converting page source into Beautiful soup object
soup=bs(ps,"html.parser")

#Extracting the reviews present in div html_tag having class containing "text" in its value
reviews = soup.findAll("div",attrs={"class","text"})
for i in range(len(reviews)):
    reviews[i] = reviews[i].text
 

# Creating a data frame 
import pandas as pd
movie_reviews = pd.DataFrame(columns = ["reviews"])
movie_reviews["reviews"] = reviews

movie_reviews.to_csv("movie_reviews.csv",encoding="utf-8")

reviews_Moana = ' '.join(reviews)

import re
from nltk.corpus import stopwords


# Removing unwanted symbols incase if exists
ip_rev_string = re.sub("[^A-Za-z" "]+"," ",reviews_Moana).lower()
ip_rev_string = re.sub("[0-9" "]+"," ",reviews_Moana)

# words that contained in iphone XR reviews
ip_reviews_words = ip_rev_string.split(" ")

#TFIDF
from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer=TfidfVectorizer(ip_reviews_words,use_idf=True,ngram_range=(1, 3))
X=vectorizer.fit_transform(ip_reviews_words)

with open("E:/ADM/Excelr solutions/DS assignments/Text mining/stop.txt","r") as sw:
    stopwords = sw.read()

stopwords = stopwords.split("\n")

ip_reviews_words = [w for w in ip_reviews_words if not w in stopwords]


# Joinining all the reviews into single paragraph 
ip_rev_string = " ".join(ip_reviews_words)

# WordCloud can be performed on the string inputs. That is the reason we have combined 
# entire reviews into single paragraph
# Simple word cloud

##plotting wordcloud on TFIDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt

wordcloud_ip = WordCloud(
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_rev_string)

plt.imshow(wordcloud_ip)

# positive words # Choose the path for +ve words stored in system
with open("E:/ADM/Excelr solutions/DS assignments/Text mining/positive-words.txt","r") as pos:
  poswords = pos.read().split("\n")
  
poswords = poswords[36:]


# negative words  Choose path for -ve words stored in system
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
                      background_color='black',
                      width=1800,
                      height=1400
                     ).generate(ip_pos_in_pos)

plt.imshow(wordcloud_pos_in_pos)
