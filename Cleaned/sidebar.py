#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
31 Mar 2018
"""

#Imports
from __future__ import division
import datetime
import sys
import time
import weekends
import webscraper as ws
import templates as tp

class Sidebar():

    def __init__(self, sub):
        self.sub = sub
    
    def insertText(self, text, beginMarker=-1, endMarker=-1):
        try:
            oldSidebar = self.sub.mod.settings()["description"]
            if beginMarker == -1 and endMarker == -1:
                return False
            elif beginMarker == -1:
                endIndex = oldSidebar.find(endMarker)
                if endIndex == -1:
                    return False
                newSidebar = oldSidebar[:endIndex] + text + oldSidebar[endIndex:]
            elif endMarker == -1:
                beginIndex = oldSidebar.find(beginMarker)+len(beginMarker)
                if beginIndex == -1:
                    return False
                newSidebar = oldSidebar[:beginIndex] + text + oldSidebar[beginIndex:]
            else:
                beginIndex = oldSidebar.find(beginMarker)+len(beginMarker)
                endIndex = oldSidebar.find(endMarker)
                if beginIndex == -1 or endIndex == -1:
                    return False
                newSidebar = oldSidebar[:beginIndex] + text + oldSidebar[endIndex:]
            self.sub.mod.update(description=newSidebar)
        except Exception as e:
            print("Error in insertText: {}".format(e))
            return False
        
    def updateCountdown(self, nextRace, prevRace):
        #Updates the countdown in the sidebar of the subreddit
        print("Updating the countdown in the F1 sidebar")
        beginMarker = "[](/countDownBegin)"
        endMarker = "[](/countDownEnd)"
        try:
            oldSidebar = subreddit.mod.settings()["description"]
            startIndex = oldSidebar.find(beginMarker)+len(beginMarker)
            endIndex = oldSidebar.find(endMarker)
            if startIndex == -1 or endIndex == -1:
                return False
            elif currentTime < (prevRace + datetime.timedelta(hours=2, minutes=30)) and prevRace < currentTime:
                countdown = "In progress"
                newSidebar = oldSidebar[:startIndex]+countdown+oldSidebar[endIndex:]
                subreddit.mod.update(description=newSidebar)
            else:
                delta = nextRace - currentTime
                hours = int((delta.seconds - delta.seconds%3600)/3600)
                minutes = int((delta.seconds%3600)/60)
                countdown = "{0} day{1}, {2} hour{3} and {4} minute{5}".format(delta.days, "s"*(delta.days != 1), hours, "s"*(hours != 1),  minutes, "s"*(minutes != 1))
                newSidebar = oldSidebar[:startIndex]+countdown+oldSidebar[endIndex:]
                subreddit.mod.update(description=newSidebar)
            print("Sucessfully updated the sidebar")
        except Exception as e:
            print "Error in updateCounter: {}".format(e)