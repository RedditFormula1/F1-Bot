#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/motorsportsstreams
Written by /u/Redbiertje
14 June 2017
"""

#Imports
from __future__ import division
import numpy as np
import datetime
import sys
import time
import bottaswmr


#Define important stuff
moderators = ["_Kierz_", "BottasWMR", "Thatoneguyone", "rubennaatje", "Maxnl9", "Redbiertje", "MSS-Bot", "wirelessflyingcord", "johnnyracer24", "5trid3r", "Tramunzenegger", "okaythistimeitsnotme"]

class Event:
    #Contains all data important to an event
    def __init__(self):
        self.name = "Event"
        self.title = "Title"
        self.duration = 120
        self.date = datetime.datetime.utcnow()

def weekdayToWord(i):
    #Turns the number of day of the week into a three-letter string
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    return weekdays[i]

def weekdayToFullWord(i):
    #Turns the number of day of the week into the full word
    weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    return weekdays[i]

def monthToWord(i):
    #Turns the number of month of the year into a three-letter string
    months = ["Err", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    return months[i]

def upcomingEvents(limit=-1, minus=datetime.timedelta(minutes=1)):
    #Returns a list of upcoming events
    global events
    eventList = sorted(events, key = lambda x: x.date)
    output = []
    for i in range(len(eventList)):
        if len(output) == limit:
            return output
        else:
            if currentTime < (eventList[i].date + minus):
                output.append(eventList[i])
    return output

def retrieveEventData(subreddit):
    #Pulls event data from the subreddit wiki
    global events
    print("Retrieving event information from the wiki")
    i = -1
    try:
        wikiContent = subreddit.wiki['schedule'].content_md
        wikiRows = wikiContent.split("\r\n")
        events = []
        for i in range(len(wikiRows[4:])):
            event = Event()
            row = wikiRows[i+4]
            if row != "":
                columns = row[1:-1].split("|")
                dateStringList = columns[0].split("-")
                timeStringList = columns[1].split(":")
                event.duration = datetime.timedelta(minutes = int(columns[2]))
                event.title = columns[3]
                event.name = columns[4]
                event.date = datetime.datetime(int(dateStringList[0]), int(dateStringList[1]), int(dateStringList[2]), int(timeStringList[0]), int(timeStringList[1]))
                events.append(event)
        print("Successfully retrieved data")
        return True, True
    except Exception as e:
        print("Error in retrieveEventData: {}".format(e))
        return i, e

def scheduledPostChecker(motorsportsstreams, motorsportsreplays):
    #Checks if any posts should be submitted
    global currentTime
    global prevTime
    print("Checking if anything should be posted")
    try:
        for event in upcomingEvents(minus=datetime.timedelta(days=2)):
            streamTime = event.date - datetime.timedelta(hours=2)
            replayTime = event.date
            finishTime = event.date + event.duration
            deleteTime = finishTime + datetime.timedelta(hours=2)
            if streamTime < currentTime and (prevTime < streamTime or prevTime == streamTime):
                print("Posting a thread to /r/motorsportsstreams")
                post = postToSubreddit(motorsportsstreams, event, "stream")
                post.mod.flair(text="Upcoming", css_class="upcoming")
                print("Successfully posted a thread")
            if replayTime < currentTime and (prevTime < replayTime or prevTime == replayTime):
                print("Posting a thread to /r/motorsportsreplays")
                post = postToSubreddit(motorsportsreplays, event, "replay")
                print("Successfully posted a thread")
                for oldPost in r.user.me().new(limit=25):
                    if oldPost.title == "[{0:02d}:{1:02d} GMT] {2}".format(event.date.hour, event.date.minute, event.title) and oldPost.subreddit == "motorsportsstreams":
                        print("Flairing a post as 'Live'")
                        oldPost.mod.flair(text="Live", css_class="live")
            if finishTime < currentTime and (prevTime < finishTime or prevTime == finishTime):
                for oldPost in r.user.me().new(limit=25):
                    if oldPost.title == "[{0:02d}:{1:02d} GMT] {2}".format(event.date.hour, event.date.minute, event.title) and oldPost.subreddit == "motorsportsstreams":
                        print("Flairing a post as 'Finished'")
                        oldPost.mod.flair(text="Finished", css_class="finished")
            if deleteTime < currentTime and (prevTime < deleteTime or prevTime == deleteTime):
                for oldPost in r.user.me().new(limit=25):
                    if oldPost.title == "[{0:02d}:{1:02d} GMT] {2}".format(event.date.hour, event.date.minute, event.title) and oldPost.subreddit == "motorsportsstreams":
                        print("Removing a post for being finished")
                        oldPost.mod.remove()
                
    except Exception as e:
        print("Error in scheduledPostChecker: {}".format(e))

def postToSubreddit(subreddit, event, word):
    #Posts a discussion post to the subreddit
    try:
        title = "[{0:02d}:{1:02d} UTC] {2}".format(event.date.hour, event.date.minute, event.title)
        if word == "stream":
            content = "#Stream thread for the {0}\n\n---\n\nDISCORD: Please use our discord server for communication instead of the comments section below, where streams should go instead. [Click here to join our discord](https://discordapp.com/invite/2knJy8R)\n\n---\n\n**COMMENT STREAMS BELOW, BUT MAKE SURE YOU FOLLOW ALL THE RULES (FOUND ON THE SIDEBAR) OTHERWISE YOUR COMMENTS WILL BE REMOVED, AND YOU MAY BE BANNED**\n\n**ONE LINK PER COMMENT. NO OTHER COMMENTS ALLOWED.**".format(event.name)
        else:
            content = "#Replay thread for the {0}".format(event.name)
        post = subreddit.submit(title, content, send_replies=False)
        post.mod.distinguish(how="yes", sticky=False)
        return post
    except Exception as e:
        print("Error in postToSubreddit: {}".format(e))
        
def updateSidebarSchedule(subreddit):
    #Updates the schedule in the sidebar
    print("Updating the schedule in the sidebar")
    beginMarker = "[](/beginSchedule)"
    endMarker = "[](/endSchedule)"
    try:
        oldSidebar = subreddit.mod.settings()["description"]
        startIndex = oldSidebar.find(beginMarker)+len(beginMarker)
        endIndex = oldSidebar.find(endMarker)
        if startIndex == -1 or endIndex == -1:
            return False
        else:
            schedule = "\n\n|Upcoming events|\n|:-:|"
            eventList = upcomingEvents(limit = 5)
            for i in range(len(eventList)):
                event = eventList[i]
                schedule += "\n|{0} {1} {2}, {3:02d}:{4:02d} GMT|\n|{5}|".format(weekdayToWord(event.date.weekday()), event.date.day, monthToWord(event.date.month), event.date.hour, event.date.minute, event.title)
            if schedule == "\n\n|Upcoming events|\n|:-:|":
                schedule = "\n\n|Upcoming events|\n|:-:|\n|There are no events scheduled|"
            newSidebar = oldSidebar[:startIndex]+schedule+oldSidebar[endIndex:]
            subreddit.mod.update(description=newSidebar)
        print("Sucessfully updated the sidebar")
    except Exception as e:
        print("Error in updateSidebarSchedule: {}".format(e))

def checkMail(subreddit):
    #Checks mailbox
    print("Checking mail")
    messages = r.inbox.unread()
    counter = 0
    try:
        for message in messages:
            print("Reading a message")
            message.mark_read()
            counter += 1
            if message.author in moderators and message.body.lower() == "verify":
                success, e = retrieveEventData(subreddit)
                if success == -1:
                    message.reply("It looks like something went wrong really bad.\n\nError: {}".format(e))
                elif success == True:
                    message.reply("It looks like everything has been filled in correctly")
                else:
                    message.reply("Something is wrong on row {0}\n\nError: {1}".format(success+1, e))
            if counter == 30 and lastAlert + datetime.timedelta(minutes=10) < currentTime:
                lastAlert = currentTime
                print("Alerting mod team of inbox overload")
                protectInbox()
                subreddit.message("MSS-Bot: Overload alert", "This is an automated message to let you know that the bot's inbox is being flooded. Please take the following steps:\n\n1. Make sure that all recent posts by /u/MSS-Bot have the inbox replies setting disabled.\n2. Open /u/MSS-Bot's inbox, and mark all messages as read.")
    except Exception as e:
        print("Error in checkMail: {}".format(e))
    print("Finished checking mail")

        
def protectInbox():
    #Function to protect the inbox from overflowing
    try:
        lastPosts = r.user.me().submissions.new(limit=10)
        for post in lastPosts:
            post.disable_inbox_replies()
    except Exception as e:
        print("Error in protectInbox: {}".format(e))
        return False

retrieveEventData(MSS)
updateSidebarSchedule(MSS)
updateSidebarSchedule(MSR)
scheduledPostChecker(MSS, MSR)
checkMail(MSS)

iter_idx += 1
if iter_idx % 20 == 0:
    bottaswmr.get_games()
prevTime = currentTime
time.sleep(25)
