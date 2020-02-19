#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This is by far the most retarded piece of code I've ever had to write. Thanks @f1debrief.
Written by /u/Redbiertje
19 Feb 2020
"""

#Includes
from __future__ import division
import numpy as np
import botData as bd
import tweepy

def get_tweets(max_id=False):
    #Apparently you can't just give an absurdly high max_id by default
    if max_id:
        return twitter.user_timeline("f1debrief", since_id="1230039800947859457", max_id=max_id, tweet_mode="extended")
    else:
        return twitter.user_timeline("f1debrief", since_id="1230039800947859457", tweet_mode="extended")

#Define output filename
out_name = 'stints.csv'

#Log into Twitter API
auth = tweepy.OAuthHandler(bd.consumer_key, bd.consumer_secret)
auth.set_access_token(bd.access_token, bd.access_token_secret)
twitter = tweepy.API(auth)
print("Successfully logged in!")

#Prepare output file
output_file = open(out_name, 'w')

#Obtain all tweets
tweets = []
new_tweets = get_tweets()
while len(new_tweets) > 1:
    for t in new_tweets:
        print(t.id)
        tweets.append(t.full_text)
    max_id = str(int(new_tweets[-1].id)-1)
    new_tweets = get_tweets(max_id)

#Iterate over all tweets
for tweet in tweets:
    #If it contains stint information
    if "Stint του" in tweet:
        #Obtain driver information
        driver_start = tweet.find("του ") + 4
        driver_end = tweet.find(" (")
        driver = tweet[driver_start:driver_end]
        
        #Obtain tyre information
        tyre_start = tweet.find(" (")+2
        tyre_end = tweet.find(") ")
        tyre = tweet[tyre_start:tyre_end]
        
        #Obtain stint times
        stint_start = tweet.find("out")+3
        stint_end = tweet.find("in\n")
        stint_end2 = tweet.find("#D")
        if stint_end == -1:
            stint = tweet[stint_start:stint_end2].strip()
        else:
            stint = tweet[stint_start:stint_end].strip()
        stint = stint.replace("&lt;==", "") #Because the dude ones used a '<=='
        stint = stint.replace(" ", "") #Because the dude separates minutes from seconds with a : and a space
        times = stint.split("\n")
        line = "{},{}".format(driver, tyre)
        for time in times:
            line += ",{}".format(time)
                    
        #Write line to file
        output_file.write(line+"\n")

#Close file
output_file.close()
print("Successfully completed!")
