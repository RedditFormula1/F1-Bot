#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
16 March 2017
"""

#Imports
from __future__ import division
import datetime
import botData as bd
import numpy as np
import time
import praw
import pyowm
import os
import tweepy
import sys

#Set correct filepath
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Login
r = praw.Reddit(client_id=bd.app_id, client_secret=bd.app_secret, password=bd.password, user_agent=bd.app_user_agent, username=bd.username)
if(r.user.me()==bd.username):
    print("Successfully logged in")
subreddit = r.subreddit("formula1")
private_subreddit = r.subreddit("formula1bot")
formula1exp = r.subreddit("formula1exp")
redbiertje = r.redditor("Redbiertje")

#Open Weather API
owm = pyowm.OWM(bd.weather_api)

#Open Twitter API
auth = tweepy.OAuthHandler(bd.consumer_key, bd.consumer_secret)
auth.set_access_token(bd.access_token, bd.access_token_secret)
twitter = tweepy.API(auth)

#Set start states
global prevTime
global currentTime
prevTime = datetime.datetime.utcnow()
currentTime = datetime.datetime.utcnow()
lastAlert = prevTime-datetime.timedelta(minutes=11)
lastCommand = [1, 2]
alertState = "normal"
boot = True
qualiResultTime = prevTime-datetime.timedelta(minutes=1)
raceResultTime = prevTime-datetime.timedelta(minutes=1)
lastQ2Time = prevTime-datetime.timedelta(minutes=10)
trackedComments = np.array([["Blank", None, None, None, None, None, None, None, None, None, None, None]])

#Keep the bot alive
while True:
    try:
        currentTime = datetime.datetime.utcnow()
        print("----------[{0:02d}:{1:02d}:{2:02d}]-----------".format(currentTime.hour, currentTime.minute, currentTime.second))
        exec(open("injected.py").read())
    except Exception as e:
        print("Major error in loop: {}".format(e))
        time.sleep(5)
