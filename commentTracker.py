#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
18 Sep 2017
"""

#Imports
from __future__ import division
import numpy as np
import datetime
from time import time

def switchHidingTime(subreddit):
    rotation_dict = {'0': 30, '30': 60, '60': 0}
    try:
        hide_mins = str(subreddit.mod.settings()["comment_score_hide_mins"])
        subreddit.mod.update(comment_score_hide_mins=rotation_dict[hide_mins])
        return rotation_dict[hide_mins]
    except Exception as e:
        print("Error in switchHidingTime: {}".format(e))
        return None

def storeComment(comment):
    print("Storing comment")
    try:
        data_file = open("data/commentdata.dat", "a")
        data_file.write("\n{0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}, {8}, {9}, {10}".format(comment[0], comment[1], comment[3], comment[4], comment[5], comment[6], comment[7], comment[8], comment[9], comment[10], comment[11]))
        data_file.close()
    except Exception as e:
        print("Error in storeComment: {}".format(e))

def trackComments(reddit, subreddit, trackedComments, currentTime, prevTime):
    try:
        t_start = time()
        #Catch bugs
        try:
            print(trackedComments[1:3, :])
            print("Current tracking {} comments".format(len(trackedComments)))
        except:
            trackedComments = np.array([["Blank", None, None, None, None, None, None, None, None, None, None, None]])
        
        #Check current amount of minutes votes are hidden
        hide_mins = subreddit.mod.settings()["comment_score_hide_mins"]
        
        #Retrieve old data from file
        old_data = np.loadtxt("data/commentdata.dat", comments="#", dtype='str', delimiter=', ')
        
        #Add these IDs to the list of currently tracked IDs
        old_IDs = np.concatenate((trackedComments[:, 0], old_data.T[0]))
        
        #Retrieve the last 5 comments
        newCount = 0
        for comment in subreddit.comments(limit=10):
            #If new comment, add to tracking list
            if comment.id not in old_IDs:
                newCount += 1
                trackedComments = np.append(trackedComments, [[comment.id, comment.created_utc, datetime.datetime.utcfromtimestamp(comment.created_utc), hide_mins, None, None, None, None, None, None, None, None]], axis=0)
        print("Added {} comments to tracking list".format(newCount))
        
        #Go through all tracked comments
        mask = np.ones(len(trackedComments), dtype=bool)
        for idx, comment in enumerate(trackedComments):
            #If it is at the given intervals, check score and store
            if comment[1] != None:
                #Check if comment still exists, else remove from tracking list
                try:
                    reddit_comment = reddit.comment(comment[0])
                    for i in range(1, 10):
                        if comment[2]+datetime.timedelta(minutes=15*i) < currentTime and (prevTime < comment[2]+datetime.timedelta(minutes=15*i) or prevTime == comment[2]+datetime.timedelta(minutes=15*i)):
                            if i==9:
                                mask[idx] = False
                                storeComment(comment)
                            elif i==4:
                                if comment[3] == hide_mins:
                                    comment[i+3] = reddit_comment.score
                                else:
                                    mask[idx] = False
                            else:
                                comment[i+3] = reddit_comment.score
                except Exception as e:
                    mask[idx] = False
        print("Tracking comments took {:.1f} seconds.".format(time()-t_start))
        return trackedComments[mask]
    except Exception as e:
        print("Error in trackComments: {}".format(e))