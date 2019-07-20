#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
11 Jan 2018
"""

#Imports
from __future__ import division
import traceback
import datetime
import sys
import time
import numpy as np
import weekends
import webscraper as ws
import commentTracker as ct
import auxiliary as aux
import subreddit as sub
import templates as tp


#Reload modules
reload(sys)
reload(weekends)
reload(ws)
reload(tp)
reload(ct)
reload(sub)
reload(aux)
sys.setdefaultencoding('utf-8')

#Define important stuff
currentYear = 2019
prevYear = 2018
moderators = ["ddigger", "Mulsanne", "HeikkiKovalainen", "halfslapper", "empw", "whatthefat", "Redbiertje", "jeppe96", "BottasWMR", "flipjj", "Effulgency", "Blanchimont", "elusive_username"]
authorized = ["F1-Official", "F1_Research", "Greenbiertje", "sbnufc"]

def scheduleChecker(subreddit, fc):
    """
    Checks if any posts should be submitted
    """
    global currentTime
    global prevTime
    global owm
    
    #Define raceweekend boolean
    isRaceWeekend = False
    
    #Iterate over all weekends
    for weekend in weekends.allWeekends:
        #Define at what time each session thread should be posted
        fp1Time = weekend.fp1Time - datetime.timedelta(minutes=30)
        fp2Time = weekend.fp2Time - datetime.timedelta(minutes=30)
        fp3Time = weekend.fp3Time - datetime.timedelta(minutes=30)
        qualiTime = weekend.qualiTime - datetime.timedelta(hours=1)
        preraceTime = weekend.raceTime - datetime.timedelta(hours=3)
        raceTime = weekend.raceTime - datetime.timedelta(minutes=15)
        
        #Defines the race weekend status, i.e. the day of FP1 to the day of the race
        raceWeekendBeginTime = weekend.fp1Time - datetime.timedelta(hours=weekend.fp1Time.hour)
        raceWeekendEndTime = weekend.raceTime + datetime.timedelta(hours=(24 - weekend.raceTime.hour))

        if raceWeekendBeginTime < currentTime and currentTime < raceWeekendEndTime:
            raceWeekend = True
        
        #Define at what time the sidebar should be updated
        updateTime1 = weekend.raceTime + datetime.timedelta(hours=2, minutes=15)
        updateTime2 = weekend.raceTime + datetime.timedelta(hours=3)
        
        #Define at which times Tweets should be posted
        twitterTimes = [weekend.fp1Time - datetime.timedelta(hours=1), weekend.fp2Time - datetime.timedelta(hours=1), weekend.fp3Time - datetime.timedelta(hours=1), weekend.qualiTime - datetime.timedelta(hours=1), weekend.raceTime - datetime.timedelta(hours=1)]
        
        #Post the Weekend Hub if required
        try:
            if weekend.hubTime < currentTime and (prevTime < weekend.hubTime or prevTime == weekend.hubTime):
                print("Posting a weekend hub")
                post = subreddit.postToSubreddit(weekend, "Weekend Hub", owm=owm, fc=fc)
                if settings["newFormat"]:
                    post.mod.sticky(bottom=False)
                print("Successfully posted a weekend hub")
                print("Updating top bar")
                subreddit.sidebar.updateTopBar(post, weekend, "Hub")
                print("Successfully updated the top bar")
                post.mod.flair(text="Weekend Hub", css_class="hub")
        except Exception as e:
            print("Error in scheduleChecker (flag 1): {}".format(e))
        
        #If the new format is requested
        if settings["newFormat"]:
            try:
                if fp1Time < currentTime and (prevTime < fp1Time or prevTime == fp1Time):
                    print("Posting a FP1 live thread")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 1", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a FP1 live discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP1 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 1", css_class="practice")
                    post.mod.suggested_sort(sort="new")
                    print("Posting a Free Practice discussion thread")
                    post = subreddit.postToSubreddit(weekend, "Free Practice", live=False)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a Free Practice discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.1): {}".format(e))
            try:
                if fp2Time < currentTime and (prevTime < fp2Time or prevTime == fp2Time):
                    print("Posting a FP2 live thread")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 2", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a FP2 discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP2 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 2", css_class="practice")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.2): {}".format(e))
            try:
                if fp3Time < currentTime and (prevTime < fp3Time or prevTime == fp3Time):
                    print("Posting a FP3 discussion")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 3", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a FP3 discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP3 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 3", css_class="practice")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.3): {}".format(e))
            try:
                if qualiTime < currentTime and (prevTime < qualiTime or prevTime == qualiTime):
                    print("Posting a qualifying live thread")
                    post = subreddit.postToSubreddit(weekend, "Qualifying", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a qualifying live thread")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "Q ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Qualifying", css_class="qualifying")
                    post.mod.suggested_sort(sort="new")
                    print("Posting a qualifying discussion")
                    post = subreddit.postToSubreddit(weekend, "Qualifying")
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a qualifying discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "Q ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Qualifying", css_class="qualifying")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.4): {}".format(e))
            try:
                if preraceTime < currentTime and (prevTime < preraceTime or prevTime == preraceTime):
                    print("Posting a race live thread")
                    post = subreddit.postToSubreddit(weekend, "Race", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a race live thread")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "Race ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Race", css_class="race")
                    post.mod.suggested_sort(sort="new")
                    print("Posting a race discussion")
                    post = subreddit.postToSubreddit(weekend, "Race")
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a race discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "Race ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Race", css_class="race")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.5): {}".format(e))
                
        else: #Old format
            try:
                if fp1Time < currentTime and (prevTime < fp1Time or prevTime == fp1Time):
                    print("Posting a FP1 discussion")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 1")
                    print("Successfully posted a FP1 discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP1")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 1", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.1): {}".format(e))
            try:
                if fp2Time < currentTime and (prevTime < fp2Time or prevTime == fp2Time):
                    print("Posting a FP2 discussion")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 2")
                    print("Successfully posted a FP2 discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP2")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 2", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.2): {}".format(e))
            try:
                if fp3Time < currentTime and (prevTime < fp3Time or prevTime == fp3Time):
                    print("Posting a FP3 discussion")
                    post = subreddit.postToSubreddit(weekend, "Free Practice 3")
                    print("Successfully posted a FP3 discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "FP3")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 3", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.3): {}".format(e))
            try:
                if qualiTime < currentTime and (prevTime < qualiTime or prevTime == qualiTime):
                    print("Posting a qualifying discussion")
                    post = subreddit.postToSubreddit(weekend, "Qualifying")
                    print("Successfully posted a qualifying discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "Q")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Qualifying", css_class="qualifying")
                    if settings["suggestedNew"]:
                        post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.4): {}".format(e))
            try:
                if preraceTime < currentTime and (prevTime < preraceTime or prevTime == preraceTime):
                    print("Posting a pre-race discussion")
                    post = subreddit.postToSubreddit(weekend, "Pre Race")
                    print("Successfully posted a pre-race discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "PR")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Pre Race", css_class="race")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.5): {}".format(e))
            try:
                if raceTime < currentTime and (prevTime < raceTime or prevTime == raceTime):
                    print("Posting a race discussion")
                    post = subreddit.postToSubreddit(weekend, "Race", fc=fc)
                    print("Successfully posted a race discussion")
                    print("Updating top bar")
                    subreddit.sidebar.updateTopBar(post, weekend, "R")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Race", css_class="race")
                    if settings["suggestedNew"]:
                        post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.6): {}".format(e))
        try:
            if (updateTime1 < currentTime and (prevTime < updateTime1 or prevTime == updateTime1)) or (updateTime2 < currentTime and (prevTime < updateTime2 or prevTime == updateTime2)):
                print("Updating the sidebar")
                race = subreddit.sidebar.updateSidebarInfo()
                if race == False:
                    print("The bot failed while updating the information in the sidebar.")
                else:
                    print("Updating the information in the F1 sidebar for the {}".format(race))
        except Exception as e:
            print("Error in scheduleChecker (flag 4): {}".format(e))
        try:
            if weekend.dadTime < currentTime and (prevTime < weekend.dadTime or prevTime == weekend.dadTime):
                print("Posting a day-after-debrief discussion")
                post = subreddit.postToSubreddit(weekend, "Day after Debrief")
                if settings["newFormat"]:
                    post.mod.sticky(bottom=False)
                print("Successfully posted a day-after-debrief discussion")
                print("Updating top bar")
                subreddit.sidebar.updateTopBar(post, weekend, "DaD")
                print("Successfully updated the top bar")
                post.mod.flair(text="Day after Debrief", css_class="feature")
        except Exception as e:
            print("Error in scheduleChecker (flag 5): {}".format(e))
            
        #Iterate over the Tweet times
        events = ["Free Practice 1 for the {} Grand Prix".format(weekend.namean), "Free Practice 2 for the {} Grand Prix".format(weekend.namean), "Free Practice 3 for the {} Grand Prix".format(weekend.namean), "Qualifying for the {} Grand Prix".format(weekend.namean), "The {} Grand Prix".format(weekend.namean)]
        for i in range(len(twitterTimes)):
            try:
                #Find the relevant Tweet to post
                if twitterTimes[i] < currentTime and (prevTime < twitterTimes[i] or prevTime == twitterTimes[i]):
                    print("Posting a tweet")
                    
                    #If not testing, proceed with tweeting
                    if not settings["testingMode"]:
                        tweet = twitter.update_status("Reminder: {0} starts in one hour. #{1}GP".format(events[i], weekend.namean.replace(" ", "")))
                    print("Successfully posted a tweet")
            except Exception as e:
                print("Error in scheduleChecker (flag 6): {}".format(e))
    #Iterate over all tech talk threads of the year
    for techDate in weekends.techTalks:
        try:
            #If a tech talk thread should be posted
            if techDate < currentTime and (prevTime < techDate or prevTime == techDate):
                print("Posting a Tech Talk thread")
                
                #Construct title and content
                title = "Tech Talk {}".format(aux.weekdayToFullWord(techDate.weekday()))
                content = content = "### Welcome to the Tech Talk {0}!\n\nIn this weekly thread, we'd like to give you all a place to discuss technical aspects of the sport. Discussion topics could include characteristics of the cars; recent or planned aero, chassis, engine, and tyre developments; analysis of images; and model-based or data-based predictions. We hope that this will promote more detailed technical discussions in the subreddit.\n\nLow effort comments, such as memes and jokes will be deleted, as will off-topic content, such as discussions centered on drivers. We also discourage superficial comments that contain no analysis or reasoning in this thread.\n\n#### Interesting links\n\nBe sure to check our /r/F1Technical for more in-depth analysis.".format(aux.weekdayToFullWord(techDate.weekday()))
                
                #Submit to subreddit
                post = subreddit.sub.submit(title, content, send_replies=False)
                
                #Attempts to unsticky other posts
                try:
                    checkPost = subreddit.sub.sticky(number=2)
                    subreddit.sub.sticky(number=1).mod.sticky(state=False)
                except Exception as e:
                    print("Error while removing top sticky in scheduleChecker: {}".format(e))
                
                #Sticky Tech Talk Thread
                post.mod.sticky()
                print("Successfully posted a tech talk discussion")
                
                #Set correct flair
                post.mod.flair(text="Tech Talk", css_class="feature")
        except Exception as e:
            print("Error in scheduleChecker (flag 7): {}".format(e))

    #Posts Daily Discussion if race weekend is not ongoing
    try:
        if not isRaceWeekend and  currentTime.hour == weekends.ddPostTime and prevTime.hour != weekends.ddPostTime:
            print('Posting Daily Discussion')
            title = "Daily Discussion - {} {} {}".format(currentTime.day, aux.monthToWord(currentTime.month), currentTime.year)
            content = 'This thread is for general discussion of current topics in F1 and quick questions about the sport.'
            post = subreddit.sub.submit(title, content, send_replies=False)
            print("Successfully posted a daily discussion")
            post.mod.sticky(bottom=True)
            print("Successfully stickied a daily discussion")
            post.mod.flair(text="Daily Discussion", css_class="feature")
    except Exception as e:
            print("Error in scheduleChecker (flag 8): {}".format(e))

def checkMail(f1_subreddit, f1bot_subreddit, f1exp_subreddit, forecast):
    """
    Checks mailbox and takes requested actions
    """
    global lastCommand
    global lastAlert
    global qualiResultTime
    global raceResultTime
    global currentTime
    global owm
    
    print("Checking mail")
    
    #Obtain new messages
    messages = r.inbox.unread()
    
    #Initiate counter for the amount of messages
    counter = 0
    try:
        #Iterate over messages
        for message in messages:
            print("Reading a message from {0}: {1}".format(message.author, message.body))
            
            #Mark message as read
            message.mark_read()
            
            #Update counter
            counter += 1
            
            #If told to post a post-race or post-quali thread
            if message.author in moderators and message.body.lower() == "post":
            
                #Iterate over all weekends to find the relevant weekend
                for weekend in weekends.allWeekends:
                    try:
                    
                        #If it is time for the post-quali thread
                        if weekend.qualiTime < currentTime and currentTime < weekend.raceTime:
                        
                            #If the failsafe allows it
                            if lastCommand != [weekend.country, "quali"]:
                                print("Posting a post-quali discussion")
                                
                                #Check if we're not in testing mode
                                if not settings["testingMode"]:
                                    post = f1_subreddit.postToSubreddit(weekend, "Post Qualifying")
                                else:
                                    post = f1exp_subreddit.postToSubreddit(weekend, "Post Qualifying")
                                    
                                #Update failsafe first
                                lastCommand = [weekend.country, "quali"]
                                
                                #Schedule a check for the quali results in one minute
                                qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                                print("Successfully posted a post-qualifying discussion")
                                
                                #Update top bar if not in testing mode
                                print("Updating top bar")
                                if not settings["testingMode"]:
                                    f1_subreddit.updateTopBar(post, weekend, "PQ")
                                else:
                                    f1exp_subreddit.updateTopBar(post, weekend, "PQ")
                                print("Successfully updated the top bar")
                                
                                #Sticky it and add it to the Weekend Hub if not in testing mode
                                if not settings["testingMode"]:
                                    post.mod.sticky(bottom=True)
                                    addToHub(post, weekend)
                                    
                                #Inform the moderator of this splendid success
                                message.reply("Successfully posted a post-qualifying discussion\n\n{}".format(post.shortlink))
                                
                                #Set suggested sort if required
                                if settings["suggestedNew"]:
                                    setSuggestedSort("qualifying", "blank")
                                
                                #Set correct flair
                                post.mod.flair(text="Post Qualifying", css_class="post-qualifying")
                            else:
                                #If already posted, inform moderator
                                message.reply("Somebody else already posted a post-qualifying discussion")
                    except Exception as e:
                        print("Error in checkMail (flag 1): {}".format(e))
                    try:
                        #If it is time for the post-race thread
                        if weekend.raceTime < currentTime and currentTime < weekend.dadTime:
                            
                            #If the failsafe allows it
                            if lastCommand != [weekend.country, "race"]:
                                print("Posting a post-race discussion")
                                
                                #Check if we're not in testing mode
                                if not settings["testingMode"]:
                                    post = f1_subreddit.postToSubreddit(weekend, "Post Race")
                                else:
                                    post = f1exp_subreddit.postToSubreddit(weekend, "Post Race")
                                
                                #Update failsafe first
                                lastCommand = [weekend.country, "race"]
                                
                                #Schedule a check for the race results in one minute
                                raceResultTime = currentTime+datetime.timedelta(minutes=1)
                                print("Successfully posted a post-race discussion")
                                
                                #Update top bar if not in testing mode
                                print("Updating top bar")
                                if not settings["testingMode"]:
                                    f1_subreddit.updateTopBar(post, weekend, "PR")
                                else:
                                    f1exp_subreddit.updateTopBar(post, weekend, "PR")
                                print("Successfully updated the top bar")
                                
                                #Sticky it and add it to the Weekend Hub if not in testing mode
                                if not settings["testingMode"]:
                                    post.mod.sticky(bottom=True)
                                    addToHub(post, weekend)
                                
                                #Inform the moderator of this splendid success
                                message.reply("Successfully posted a post-race discussion\n\n{}".format(post.shortlink))
                                
                                #Set suggested sort if required
                                if settings["suggestedNew"]:
                                    setSuggestedSort("race", "blank")
                                
                                #Set correct flair
                                post.mod.flair(text="Post Race", css_class="post-race")
                            else:
                                #If already posted, inform moderator
                                message.reply("Somebody else already posted a post-race discussion")
                    except Exception as e:
                        print("Error in checkMail (flag 2): {}".format(e))
            
            #If told to update the weather prediction
            if message.author in moderators and message.body.lower() == "weather":
            
                #Tell the subreddit to inform its weather prediction
                fc = f1_subreddit.sidebar.updateWeatherPrediction(owm, forecast)
                
                #If something went wrong, inform the moderator
                if fc == False:
                    message.reply("Something went wrong while updating the weather prediction")
                    
                #Or tell them how great everything went
                else:
                    message.reply("Successfully updated the weather prediction\n\n/r/formula1")
                    
            #If instructed to clear the failsafe
            if message.author in moderators and message.body.lower() == "clear failsafe":
            
                #Inform the human that their message has been received
                message.reply("Successfully cleared the failsafe")
                
                #Clear the failsafe
                lastCommand = [1, 1]
            
            #If told to update the sidebar information
            if message.author in moderators and message.body.lower() == "sidebar":
            
                #Instruct the main subreddit to update its sidebar
                race = f1_subreddit.sidebar.updateSidebarInfo()
                
                #If it failed, inform the moderator
                if race == False:
                    message.reply("The bot failed while updating the information in the sidebar.")
                    
                #Or tell them how great everything went
                else:
                    message.reply("Updating the information in the F1 sidebar for the {}".format(race))
            
            #If asked for the current driver standings
            if message.author in moderators and message.body.lower() == "results":
            
                #Reply with the requested information
                message.reply(ws.driverStandings())
            
            #If asked for the upcoming starting grid
            if message.author in moderators and message.body.lower() == "grid":
            
                #Reply with the requested information
                message.reply(ws.startingGrid(prevDate()))
                
            #If told to post the qualifying results
            if message.author in moderators and message.body.lower() == "qualiresults":
                
                #Execute the relevant function
                success = postResults("qualifying")
                
                #Tell the moderator that everything went fine
                if success:
                    message.reply("Successfully posted the qualifying results")
                
                #Or not
                else:
                    message.reply("Could not post the qualifying results")
            
            #If told to post the race results
            if message.author in moderators and message.body.lower() == "raceresults":
                
                #Execute the relevant function
                success = postResults("race")
                
                #Tell the moderator that everything went fine
                if success:
                    message.reply("Successfully posted the race results")
                    
                #Or not
                else:
                    message.reply("Could not post the race results")
                    
            #If told to check if the session is finished
            if message.author in moderators and message.body.lower() == "finished":
                
                #Execute the relevant function
                finished = checkSessionFinished(f1_subreddit, "any")
                
                #Tell the moderator if not the case
                if not finished:
                    message.reply("Session has not finished yet.")
                    
            #If told to update the flair counts
            if message.author in moderators and message.body.lower() == "flairs":
                
                #Check if we're not in a race/quali session because this takes a little while
                if alertState == "normal":
                    
                    #Update the flair counts
                    f1_subreddit.updateFlairCounts(message.author)
                    
                    #Notify moderator of success
                    message.reply("Successfully updated the flair counts.\n\n/r/{}/wiki/flaircounts".format(f1_subreddit.sub.display_name))
                else:
                    message.reply("F1-Bot is currently occupied with the current qualifying/race. Please try again later.")
                    
            #It told to retrieve the traffic stats
            if (message.author in moderators or message.author in authorized) and message.body.lower() == "traffic":
                
                #Obtain traffic stats report
                trafficReport = f1_subreddit.getTrafficReport()
                
                #If successful, forward report to human
                if trafficReport:
                    message.reply(trafficReport)
                    
                #Else notify human
                else:
                    message.reply("Something went wrong while generating a traffic report. Please contact /u/Redbiertje.")
            
            #If told to update the tribute
            if (message.author in moderators or message.author in authorized) and message.subject.lower() == "tribute":
                
                #Use webscraper to download image
                filename = ws.downloadImage(message.body)
                
                #If it worked, upload image to subreddit
                if filename:
                    f1_subreddit.sub.stylesheet.upload("tribute", filename)
                    f1_subreddit.sub.stylesheet.update(f1_subreddit.sub.stylesheet().stylesheet, reason="Updating tribute")
                    
                    #Notify human
                    message.reply("Thank you very much!! It seems your image has been correctly uploaded to the subreddit.")
                else:
                    message.reply("Something went wrong. Please contact /u/Redbiertje.")
                    
            #If a LOT of new messages are in the mailbox, alert moderators
            if counter == 5+25*(alertState=="normal") and lastAlert + datetime.timedelta(minutes=10) < currentTime:
                lastAlert = currentTime
                print("Alerting mod team of inbox overload")
                f1_subreddit.sub.message("F1-Bot: Overload alert", "This is an automated message to let you know that the bot's inbox is being flooded. Please take the following steps:\n\n1. Make sure that all recent posts by /u/F1-Bot have the inbox replies setting disabled.\n2. Open /u/F1-Bot's inbox, and mark all messages as read.")
                
    except Exception as e:
        print("Error in checkMail: {}".format(e))
    #Not going to comment this bit. It's for if Reddit's mailbox system fails
    if settings["readRobust"]:
        print("Reading /r/formula1bot posts as mail")
        try:
            posts = f1bot_subreddit.new(limit=5)
            for post in posts:
                if post.title.lower() == "command":
                    postTime = datetime.datetime(1970, 1, 1)+datetime.timedelta(seconds = post.created_utc)
                    postMessage = post.selftext
                    print("Reading a message from {0}: {1}".format(post.author, post.selftext))
                    post.mod.remove()
                    if postMessage.lower() == "post":
                        for weekend in weekends.allWeekends:
                            try:
                                if weekend.qualiTime < currentTime and currentTime < weekend.raceTime:
                                    if lastCommand != [weekend.country, "quali"]:
                                        print("Posting a post-quali discussion")
                                        submittedpost = f1_subreddit.postToSubreddit(weekend, "Post Qualifying")
                                        submittedpost.mod.sticky(bottom=False)
                                        qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                                        print("Successfully posted a post-qualifying discussion")
                                        print("Updating top bar")
                                        f1_subreddit.sidebar.updateTopBar(submittedpost, weekend, "PQ")
                                        print("Successfully updated the top bar")
                                        post.reply("Successfully posted a post-qualifying discussion\n\n{}".format(submittedpost.shortlink))
                                        lastCommand = [weekend.country, "quali"]
                                        if settings["suggestedNew"]:
                                            setSuggestedSort("qualifying", "blank")
                                        post.mod.flair(text="Post Qualifying", css_class="post-qualifying")
                                    else:
                                        message.reply("Somebody else already posted a post-qualifying discussion")
                            except Exception as e:
                                print("Error in robust checkMail (flag 1): {}".format(e))
                            try:
                                if weekend.raceTime < currentTime and currentTime < weekend.dadTime:
                                    if lastCommand != [weekend.country, "race"]:
                                        print("Posting a post-race discussion")
                                        submittedpost = f1_subreddit.postToSubreddit(weekend, "Post Race")
                                        submittedpost.mod.sticky(bottom=False)
                                        raceResultTime = currentTime+datetime.timedelta(minutes=1)
                                        print("Successfully posted a post-race discussion")
                                        print("Updating top bar")
                                        f1_subreddit.sidebar.updateTopBar(submittedpost, weekend, "PR")
                                        print("Successfully updated the top bar")
                                        message.reply("Successfully posted a post-race discussion\n\n{}".format(submittedpost.shortlink))
                                        lastCommand = [weekend.country, "race"]
                                        if settings["suggestedNew"]:
                                            setSuggestedSort("race", "blank")
                                        post.mod.flair(text="Post Race", css_class="post-race")
                                    else:
                                        message.reply("Somebody else already posted a post-race discussion")
                            except Exception as e:
                                print("Error in robust checkMail (flag 2): {}".format(e))
                    if postMessage.lower() == "weather":
                        fc = f1_subreddit.sidebar.updateWeatherPrediction(owm, forecast)
                        if fc == False:
                            post.reply("Something went wrong while updating the weather prediction")
                        else:
                            post.reply("Successfully updated the weather prediction\n\n/r/formula1")
                    if postMessage.lower() == "clear failsafe":
                        post.reply("Successfully cleared the failsafe")
                        lastCommand = [1, 1]
                    if postMessage.lower() == "sidebar":
                        race = f1_subreddit.sidebar.updateSidebarInfo()
                        if race == False:
                            post.reply("The bot failed while updating the information in the sidebar.")
                        else:
                            post.reply("Updating the information in the F1 sidebar for the {}".format(race))
        except Exception as e:
            print("Error in robust checkMail: {}".format(e))
    print("Finished checking mail")
    
def checkSessionFinished(subreddit, session):
    """
    Checks if a given session has completed, and submits the post-session thread if required
    """
    
    #Obtain global variables
    global lastCommand
    global lastQ2Time
    global qualiResultTime
    global raceResultTime
    global currentTime
    global owm
    
    try:
        print("Checking if the session is finished")
        
        #Check which session should be finished
        if session == "quali":
            weekends = [aux.nextDate()]
        elif session == "race":
            weekends = [aux.prevDate()]
        else:
            weekends = [aux.prevDate(), aux.nextDate()]
        for weekend in weekends:
            
            #If it is time for a post-quali thread
            if weekend.qualiTime < currentTime and currentTime < weekend.raceTime and lastCommand != [weekend.country, "quali"]:
                
                #If the webscraper finds that it is indeed finished
                if ws.sessionFinished(session) and settings["autoPost"] and lastQ2Time+datetime.timedelta(minutes=10) < currentTime and weekend.qualiTime+datetime.timedelta(minutes=55) < currentTime:
                    
                    #Submit post-quali thread
                    print("Posting a post-quali discussion")
                    if not settings["testingMode"]:
                        post = f1_subreddit.postToSubreddit(weekend, "Post Qualifying")
                    else:
                        post = f1exp_subreddit.postToSubreddit(weekend, "Post Qualifying")
                    
                    #Update failsafe
                    lastCommand = [weekend.country, "quali"]
                    
                    #Schedule posting the quali results
                    qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                    print("Successfully posted a post-qualifying discussion")
                    
                    #Update top bar
                    print("Updating top bar")
                    if not settings["testingMode"]:
                        f1_subreddit.sidebar.updateTopBar(post, weekend, "PQ")
                    else:
                        f1exp_subreddit.sidebar.updateTopBar(post, weekend, "PQ")
                    print("Successfully updated the top bar")
                    
                    #Set correct flair
                    post.mod.flair(text="Post Qualifying", css_class="post-qualifying")
                    
                    #Sticky new thread and add it to the hub
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                        addToHub(post, weekend)
                        
                    #Set suggested sorting
                    if settings["suggestedNew"]:
                        setSuggestedSort("qualifying", "blank")
                        
                    return True
            #If it is time for a post-race thread
            if weekend.raceTime < currentTime and currentTime < weekend.dadTime and lastCommand != [weekend.country, "race"]:
                #If the webscraper finds that it is indeed finished
                if ws.sessionFinished(session) and settings["autoPost"]:
                    
                    #Submit post-race thread
                    print("Posting a post-race discussion")
                    if not settings["testingMode"]:
                        post = f1_subreddit.postToSubreddit(weekend, "Post Race")
                    else:
                        post = f1exp_subreddit.postToSubreddit(weekend, "Post Race")
                        
                    #Update failsafe
                    lastCommand = [weekend.country, "race"]
                    
                    #Schedule posting the race results
                    raceResultTime = currentTime+datetime.timedelta(minutes=1)
                    print("Successfully posted a post-race discussion")
                    
                    #Update top bar
                    print("Updating top bar")
                    if not settings["testingMode"]:
                        f1_subreddit.sidebar.updateTopBar(post, weekend, "PR")
                    else:
                        f1exp_subreddit.sidebar.updateTopBar(post, weekend, "PR")
                    print("Successfully updated the top bar")
                    
                    #Set correct flair
                    post.mod.flair(text="Post Race", css_class="post-race")
                    
                    #Sticky new thread and add it to the hub
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                        addToHub(post, weekend)
                    
                    #Set suggested sorting
                    if settings["suggestedNew"]:
                        setSuggestedSort("race", "blank")
                        
                    return True
        return False
    except Exception as e:
        print("Error in checkSessionFinished: {}".format(e))
        return False

def botState():
    """
    Checks whether the bot should act normally or if it should adapt to a race/quali mode
    """
    
    #Obtain current time
    global currentTime
    
    #Defines the state of the bot
    for weekend in weekends.allWeekends:
        if weekend.qualiTime < currentTime and currentTime < weekend.qualiTime + datetime.timedelta(hours=1, minutes=30) and lastCommand != [weekend.country, "quali"]:
            return "quali"
        elif weekend.raceTime < currentTime and currentTime < weekend.raceTime + datetime.timedelta(hours=2, minutes=30) and lastCommand != [weekend.country, "race"]:
            return "race"
    return "normal"
        
def protectInbox():
    """
    Currently unused function to protect the inbox from overflowing
    """
    try:
        #Go through last posts to disable all inbox replies
        lastPosts = r.user.me().submissions.new(limit=10)
        for post in lastPosts:
            post.disable_inbox_replies()
    except Exception as e:
        print("Error in protectInbox: {}".format(e))
        return False

def postResults(session):
    """
    Submits the results of the latest session 
    """
    try:
        print("Attempting to post results")
        
        #If the quali results should be posted
        if session == "qualifying":
            
            #Obtain relevant weekend object
            weekend = aux.nextDate()
            
            #Iterate over the most recent posts
            for oldPost in r.user.me().submissions.new(limit=15):
                try:
                    #Check if old post has the correct title
                    if oldPost.title == "{0} {1} Grand Prix - Post Qualifying Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                        
                        #Get contents and define marker
                        content = oldPost.selftext
                        beginMarker = "[](/resultsBegin)"
                        endMarker = "[](/resultsEnd)"
                        beginIndex = content.find(beginMarker)+len(beginMarker)
                        endIndex = content.find(endMarker)
                        
                        if beginMarker == -1 or endMarker == -1:
                            return False
                        
                        #Obtain results from webscraper
                        results = ws.qualiResults(weekend)
                        
                        #If results could be obtained
                        if results:
                            
                            #Replace marker with results, and save it
                            newContent = content[:beginIndex] + "\n\n---\n\n"+results + content[endIndex:]
                            oldPost.edit(newContent)
                            print("Successfully posted qualifying results")
                            return True
                        
                        else:
                            return False
                except Exception as e:
                    print("Ran into a comment")
                    
        #If the race results should be posted
        if session == "race":
            
            #Obtain relevant weekend object
            weekend = aux.prevDate()
            
            #Iterate over the most recent posts
            for oldPost in r.user.me().submissions.new(limit=15):
                try:
                    #Check if old post has the correct title
                    if oldPost.title == "{0} {1} Grand Prix - Post Race Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                        
                        #Get contents and define marker
                        content = oldPost.selftext
                        beginMarker = "[](/resultsBegin)"
                        endMarker = "[](/resultsEnd)"
                        beginIndex = content.find(beginMarker)+len(beginMarker)
                        endIndex = content.find(endMarker)
                        
                        if beginMarker == -1 or endMarker == -1:
                            return False
                        
                        #Obtain results from webscraper
                        results, flag = ws.raceResults(weekend)
                        
                        #If results could be obtained
                        if results:
                            
                            #Replace marker with results and save it
                            newContent = content[:beginIndex] + "\n\n---\n\n"+results + content[endIndex:]
                            oldPost.edit(newContent)
                            print("Successfully posted race results")
                            return flag
                        
                        else:
                            return False
                except Exception as e:
                    print("Ran into a comment ({})".format(e))
    except Exception as e:
        print("Error in postResults: {}".format(e))
        
def addToHub(post, weekend):
    """
    Adds a post to the Weekend Hub
    """
    
    #Define the two markers
    beginMarker = "[](/sessionsBegin)"
    endMarker = "[](/sessionsEnd)"
    
    try:
        print("Adding post to Weekend Hub")
        
        #Iterate over old posts to find Weekend Hub
        for oldPost in r.user.me().new(limit=15):
            try:
                #Check if post has the correct title
                if oldPost.title == "{0} {1} Grand Prix - Weekend Hub".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    
                    #Get contents and find markers
                    content = oldPost.selftext
                    beginIndex = content.find(beginMarker)+len(beginMarker)
                    endIndex = content.find(endMarker)
                    
                    #Check if any marker failed to be located
                    if beginIndex == -1 or endIndex == -1:
                        return False
                    
                    #In the case of FP1, replace the current text
                    elif post.title == "{0} {1} Grand Prix - Free Practice 1 Discussion".format(currentYear, weekend.namean):
                        #Define new Weekend Hub content
                        newContent = content[:beginIndex]+"\n\n - [{0}]({1})".format(post.title.split("-")[1].lstrip(), post.permalink)+content[endIndex:]
                    
                    #In other case, just add to the list
                    else:
                        #Define new Weekend Hub content
                        newContent = content[:endIndex]+"\n - [{0}]({1})".format(post.title.split("-")[1].lstrip(), post.permalink)+content[endIndex:]
                    
                    #Update Weekend Hub content
                    oldPost.edit(newContent)
                    print("Successfully added post to Weekend Hub")
                    return True
            except Exception as e:
                print("Ran into a comment")
    except Exception as e:
        print("Error in addToHub: {}".format(e))
        return False
    

def setSuggestedSort(session, sorting):
    """
    Sets the suggested sorting of the given session to the given sorting
    """
    try:
        #Check if the given sorting is valid
        print("Setting the suggested sort to {}".format(sorting))
        if sorting not in ["confidence", "top", "new", "controversial", "old", "random", "qa", "blank"]:
            print("Error in setSuggestedSort: Invalid sorting given.")
            return False
        
        #If it is a qualifying session
        if session == "qualifying":
            
            #Obtain relevant weekend object
            weekend = aux.nextDate()
            
            #Loop over previous posts to find the quali thread
            for oldPost in r.user.me().new(limit=5):
                
                #Check if previous post has the correct title
                if oldPost.title == "{0} {1} Grand Prix - Qualifying Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    
                    #Set suggested sorting
                    oldPost.mod.suggested_sort(sort=sorting)
                    return True
        #If it is a race
        if session == "race":
            
            #Obtain relevant weekend object
            weekend = aux.prevDate()
            
            #Loop over previous posts to find the race thread
            for oldPost in r.user.me().new(limit=5):
                
                #Check if previous post has the correct title
                if oldPost.title == "{0} {1} Grand Prix - Race Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    
                    #Set suggested sorting
                    oldPost.mod.suggested_sort(sort=sorting)
                    return True
    except Exception as e:
        print("Error in setSuggestedSort: {}".format(e))
        
def getSettings(subreddit):
    """
    Pulls the bot settings from the wiki
    """
    try:
        #Define empty dictionary
        settings = {}
        
        #Define default settings in case things go wrong
        defaultSettings = {"replaceSticky": True, "testingMode": False, "readRobust": False, "suggestedNew": True, "newFormat": False, "dailyTweet": True, "scoreThreshold": 1000, "autoPost": True, "trackComments": False}
        
        #Pull data from the wiki page
        print("Pulling bot settings from the wiki")
        wikiContent = subreddit.wiki['botsettings'].content_md
        wikiRows = wikiContent.split("\r\n")
        
        #Iterate over all lines
        for row in wikiRows:
            if row != "":
                
                #Take everything before the # (comment), and split out the setting and its value
                setting, value = tuple(row.replace(" ", "").split("#")[0].split("="))
                
                #Convert text values to Python values, and insert them into the settings dict
                if value == "True" or value == "true":
                    settings[setting] = True
                if value == "False" or value == "false":
                    settings[setting] = False
                if value.isdigit():
                    settings[setting] = int(value)
                    
        #If all settings have been obtained, return obtained settings
        if sorted(settings.keys()) == sorted(defaultSettings.keys()):
            return settings
        
        #Else return defaults
        else:
            print("Using default settings.")
            return defaultSettings
    except Exception as e:
        print("Error in pullSettings: {}".format(e))
        return False

 
#Setup the loop
alertState = botState()
settings = getSettings(subreddit)

#Create custom subreddit objects
f1_subreddit = sub.Subreddit(r, subreddit, settings)
f1bot_subreddit = sub.Subreddit(r, private_subreddit, settings)
f1exp_subreddit = sub.Subreddit(r, formula1exp, settings)

print("Current bot state: {}".format(alertState))
print("Failsafe: {}".format(lastCommand))

#On boot, get the weather forecast
if boot == True:
    boot = False
    forecast = aux.getForecast(owm)
    
#Each hour, update the weather forecast
if currentTime.hour != prevTime.hour:
    forecast = f1_subreddit.sidebar.updateWeatherPrediction(owm, forecast)

#Each day at 3 pm, post the top tweet.
if currentTime.hour == 15 and prevTime.hour == 14 and settings["dailyTweet"]:
    f1_subreddit.tweetTopPost(twitter)

#Every ten minutes, check /r/all for posts from /r/formula1
if int(currentTime.minute/10) != int(prevTime.minute/10):
    pass
    #f1_subreddit.checkAll()

#Try to post the race/quali results if necessary
if raceResultTime < currentTime and (prevTime < raceResultTime or prevTime == raceResultTime):
    weekend = aux.prevDate()
    success = postResults("race")
    if not success and raceResultTime < weekend.raceTime + datetime.timedelta(hours=6):
        raceResultTime += datetime.timedelta(minutes=1)
if qualiResultTime < currentTime and (prevTime < qualiResultTime or prevTime == qualiResultTime):
    weekend = aux.nextDate()
    success = postResults("qualifying")
    if not success and weekend.raceTime < qualiResultTime + datetime.timedelta(days=2):
        qualiResultTime += datetime.timedelta(minutes=1)

#Check /new for reposts
print("Checking for reposts")
f1_subreddit.checkReposts()
f1_subreddit.storePostTitles()

#Alert state-dependent schedule
if alertState == "normal":
    #Update the countdown
    f1_subreddit.sidebar.updateCountdown(currentTime)
    
    #Update the quote in the header
    f1_subreddit.sidebar.updateHeaderQuote()
    
    #Check the schedule
    if settings["testingMode"]:
        scheduleChecker(f1exp_subreddit, forecast)
    else:
        scheduleChecker(f1_subreddit, forecast)
        
    #Check the inbox
    checkMail(f1_subreddit, f1bot_subreddit, f1exp_subreddit, forecast)
    
    #Finish loop
    prevTime = currentTime
    print("Waiting for 10 seconds...")
    time.sleep(10)
elif alertState == "quali" or alertState == "race":
    #Update the countdown
    f1_subreddit.sidebar.updateCountdown(currentTime)
    
    #Update the quote in the header
    f1_subreddit.sidebar.updateHeaderQuote()
    
    #Check the schedule
    if settings["testingMode"]:
        scheduleChecker(f1exp_subreddit, forecast)
    else:
        scheduleChecker(f1_subreddit, forecast)
    
    #Check the inbox
    checkMail(f1_subreddit, f1bot_subreddit, f1exp_subreddit, forecast)
    
    #Check if the current session is finished
    checkSessionFinished(f1_subreddit, alertState)
    
    #Store end of this loop
    prevTime = currentTime
    
    #Repeat checking mail and session finish three more times
    for i in range(3):
        checkMail(f1_subreddit, f1bot_subreddit, f1exp_subreddit, forecast)
        checkSessionFinished(f1_subreddit, alertState)
