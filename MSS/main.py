#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/motorsportsstreams
Written by /u/Redbiertje
14 June 2017
"""

#Imports
from __future__ import division
import datetime
import botData as bd
import time
import praw
import os

#Set correct filepath
os.chdir(os.path.dirname(os.path.abspath(__file__)))

#Login
r = praw.Reddit(client_id=bd.app_id, client_secret=bd.app_secret, password=bd.password, user_agent=bd.app_user_agent, username=bd.username)
if(r.user.me()=="MSS-Bot"):
    print("Successfully logged in")
MSS = r.subreddit("motorsportsstreams")
MSR = r.subreddit("motorsportsreplays")
MSSBot = r.subreddit("mssbot")

#Set start states
prevTime = datetime.datetime.utcnow()
lastAlert = prevTime-datetime.timedelta(minutes=11)
events = []

#Keep the bot alive
while True:
    try:
        currentTime = datetime.datetime.utcnow()
        print("----------[{0:02d}:{1:02d}:{2:02d}]-----------".format(currentTime.hour, currentTime.minute, currentTime.second))
        exec(open("injected.py").read())
    except Exception as e:
        print("Major error in loop: {}".format(e))
        time.sleep(5)
