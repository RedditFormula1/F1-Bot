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
import random
import time
import weekends
import webscraper as ws
import templates as tp

#Reload modules
reload(sys)
reload(weekends)
reload(ws)
reload(tp)
sys.setdefaultencoding('utf-8')

#Define important stuff
currentYear = 2018
prevYear = 2017
moderators = ["ddigger", "Mulsanne", "HeikkiKovalainen", "halfslapper", "empw", "whatthefat", "mikejohnno", "Redbiertje", "jeppe96"]
authorized = ["F1-Official", "F1_Research", "Greenbiertje"]

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

def weatherIcon(i):
    #Maps the weather icon names from the weather API into CSS classes as used on the subreddit
    weatherIcons = {"01d": "#w01d", "02d": "#w02d", "03d": "#w03", "04d": "#w04", "09d": "#w09", "10d": "#w10d", "11d": "#w11", "13d": "#w13", "50d": "#w50", "01n": "#w01n", "02n": "#w02n", "03n": "#w03", "04n": "#w04", "09n": "#w09", "10n": "#w10n", "11n": "#w11", "13n": "#w13", "50n": "#w50"}
    return weatherIcons[i]
    
def firstCaps(string):
    #Turns the first letter of a string into upper case
    return string[0].upper() + string[1:]
    
def weatherChange(string):
    #Changes weather description from the weather API
    if string == "Heavy intensity rain":
        return "Heavy rain"
    else:
        return string

def abbrevName(string):
    initial = string.split(' ')[0][0]
    lastname = string.split(' ', 1)[1]
    return "{0}. {1}".format(initial, lastname)

def nextDate():
    #Finds the weekend object of the upcoming race
    for weekend in weekends.allWeekends:
        if currentTime < weekend.raceTime:
            return weekend
    return weekends.allWeekends[-1]

def prevDate():
    #Finds the weekend object of the last race
    for weekend in weekends.allWeekends[::-1]:
        if weekend.raceTime < currentTime:
            return weekend
    return weekends.allWeekends[0]

def updateTopBar(subreddit, post, weekend, abbrev):
    #Updates the top bar of the subreddit
    beginMarker = "[](/topBegin)"
    endMarker = "[](/topEnd)"
    try:
        oldSidebar = subreddit.mod.settings()["description"]
        startIndex = oldSidebar.find(beginMarker)+len(beginMarker)
        endIndex = oldSidebar.find(endMarker)
        if startIndex == -1 or endIndex == -1 or settings["testingMode"] == True:
            return False
        elif abbrev == "Hub":
            insertString = "[]({0})\n- [{1}]({2})".format(weekend.flag, abbrev, post.shortlink)
            newSidebar = newSidebar = oldSidebar[:startIndex]+insertString+oldSidebar[endIndex:]
            subreddit.mod.update(description=newSidebar)
        else:
            insertString = " [{0}]({1})".format(abbrev, post.shortlink)
            newSidebar = newSidebar = oldSidebar[:endIndex]+insertString+oldSidebar[endIndex:]
            subreddit.mod.update(description=newSidebar)
    except Exception as e:
        print("Error in updateTopBar: {}".format(e))

def updateCountdown(subreddit):
    #Updates the countdown in the sidebar of the subreddit
    print("Updating the countdown in the F1 sidebar")
    beginMarker = "[](/countDownBegin)"
    endMarker = "[](/countDownEnd)"
    nextRace = nextDate().raceTime
    prevRace = prevDate().raceTime
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

def postToSubreddit(subreddit, w, thread, fc=False, live=False):
    #Posts a discussion post to the subreddit
    if live:
        type = "Live Thread"
    else:
        type = "Discussion"
    try:
        qualiUTC = "{0} {1:02d}:{2:02d}".format(weekdayToWord(w.qualiTime.weekday()), w.qualiTime.hour, w.qualiTime.minute)
        raceUTC = "{0} {1:02d}:{2:02d}".format(weekdayToWord(w.raceTime.weekday()), w.raceTime.hour, w.raceTime.minute)
        fp1UTC = "{0} {1:02d}:{2:02d}".format(weekdayToWord(w.fp1Time.weekday()), w.fp1Time.hour, w.fp1Time.minute)
        fp2UTC = "{0} {1:02d}:{2:02d}".format(weekdayToWord(w.fp2Time.weekday()), w.fp2Time.hour, w.fp2Time.minute)
        fp3UTC = "{0} {1:02d}:{2:02d}".format(weekdayToWord(w.fp3Time.weekday()), w.fp3Time.hour, w.fp3Time.minute)
        
        if thread == "Weekend Hub":
            try:
                fp1Status = fc.get_weather_at(w.fp1Time)
                fp2Status = fc.get_weather_at(w.fp2Time)
                fp3Status = fc.get_weather_at(w.fp3Time)
                qualiStatus = fc.get_weather_at(w.qualiTime)
                raceStatus = fc.get_weather_at(w.raceTime)
            except Exception as e:
                print("Retrying to get a weather forecast")
                fc = getForecast()
                fp1Status = fc.get_weather_at(w.fp1Time)
                fp2Status = fc.get_weather_at(w.fp2Time)
                fp3Status = fc.get_weather_at(w.fp3Time)
                qualiStatus = fc.get_weather_at(w.qualiTime)
                raceStatus = fc.get_weather_at(w.raceTime)
            title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)
            content = tp.hub_template.format(w.round, w.country, w.flag, fp1UTC, weatherIcon(fp1Status.get_weather_icon_name()), weatherChange(firstCaps(fp1Status.get_detailed_status())), int(fp1Status.get_temperature(unit="celsius")["temp"]), int(fp1Status.get_temperature(unit="fahrenheit")["temp"]), fp2UTC, weatherIcon(fp2Status.get_weather_icon_name()), weatherChange(firstCaps(fp2Status.get_detailed_status())), int(fp2Status.get_temperature(unit="celsius")["temp"]), int(fp2Status.get_temperature(unit="fahrenheit")["temp"]), fp3UTC, weatherIcon(fp3Status.get_weather_icon_name()), weatherChange(firstCaps(fp3Status.get_detailed_status())), int(fp3Status.get_temperature(unit="celsius")["temp"]), int(fp3Status.get_temperature(unit="fahrenheit")["temp"]), qualiUTC, weatherIcon(qualiStatus.get_weather_icon_name()), weatherChange(firstCaps(qualiStatus.get_detailed_status())), int(qualiStatus.get_temperature(unit="celsius")["temp"]), int(qualiStatus.get_temperature(unit="fahrenheit")["temp"]), raceUTC, weatherIcon(raceStatus.get_weather_icon_name()), weatherChange(firstCaps(raceStatus.get_detailed_status())), int(raceStatus.get_temperature(unit="celsius")["temp"]), int(raceStatus.get_temperature(unit="fahrenheit")["temp"]))
        elif thread == "Day after Debrief":
            title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)
            content = tp.dad_template.format(w.round, w.country, w.flag, w.city)
        elif thread == "Post Qualifying" or thread == "Post Race":
            title = "{0} {1} Grand Prix - {2} Discussion".format(currentYear, w.namean, thread)
            #                                         0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23           24              25                   26                  27                  28             29              30                       31                       32                    33              34              35                  36                  37               38          39            40             41            42      43       44
            content = tp.post_session_template.format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC)
        else:
            if thread == "Pre Race" or (thread == "Race" and settings["newFormat"]):
                webscraperOutput = ws.startingGrid(w)
                if webscraperOutput == False:
                    grid = ""
                else:
                    grid = "---\n\n{}\n\n".format(webscraperOutput)
            else:
                grid = ""
            title = "{0} {1} Grand Prix - {2} {3}".format(currentYear, w.namean, thread, type)
            if settings["newFormat"]:
                #                                        0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23            24              25                   26                  27                  28             29              30                       31                       32                    33                  34              35                  36                  37               38          39            40             41            42      43      44    45
                content = tp.new_session_template.format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
            else:
                #                                        0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23            24              25                   26                  27                  28             29              30                       31                       32                    33                  34              35                  36                  37               38          39            40             41            42      43      44    45
                content = tp.old_session_template.format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
        post = subreddit.submit(title, content, send_replies=False)
        if settings["replaceSticky"] and not settings["testingMode"]:
            try:
                checkPost = subreddit.sticky(number=2)
                subreddit.sticky(number=1).mod.sticky(state=False)
            except Exception as e:
                print("Error while removing top sticky in postToSubreddit: {}".format(e))
        if not settings["newFormat"]:
            post.mod.sticky()
        return post
    except Exception as e:
        print("Error in postToSubreddit: {}".format(e))

def scheduleChecker(subreddit, fc):
    #Checks if any posts should be submitted
    global currentTime
    global prevTime
    for weekend in weekends.allWeekends:
        weatherTime = weekend.raceTime - datetime.timedelta(days=4, hours=12)
        fp1Time = weekend.fp1Time - datetime.timedelta(minutes=30)
        fp2Time = weekend.fp2Time - datetime.timedelta(minutes=30)
        fp3Time = weekend.fp3Time - datetime.timedelta(minutes=30)
        qualiTime = weekend.qualiTime - datetime.timedelta(hours=1)
        preraceTime = weekend.raceTime - datetime.timedelta(hours=3)
        raceTime = weekend.raceTime - datetime.timedelta(minutes=15)
        updateTime = weekend.raceTime + datetime.timedelta(hours=2, minutes=30)
        twitterTimes = [weekend.fp1Time - datetime.timedelta(hours=1), weekend.fp2Time - datetime.timedelta(hours=1), weekend.fp3Time - datetime.timedelta(hours=1), weekend.qualiTime - datetime.timedelta(hours=1), weekend.raceTime - datetime.timedelta(hours=1)]
        try:
            if weekend.hubTime < currentTime and (prevTime < weekend.hubTime or prevTime == weekend.hubTime):
                print("Posting a weekend hub")
                #print(fc, subreddit)
                post = postToSubreddit(subreddit, weekend, "Weekend Hub", fc)
                if settings["newFormat"]:
                    post.mod.sticky(bottom=False)
                print("Successfully posted a weekend hub")
                print("Updating top bar")
                updateTopBar(subreddit, post, weekend, "Hub")
                print("Successfully updated the top bar")
                post.mod.flair(text="Weekend Hub", css_class="hub")
        except Exception as e:
            print("Error in scheduleChecker (flag 1): {}".format(e))
        
        if settings["newFormat"]:
            try:
                if fp1Time < currentTime and (prevTime < fp1Time or prevTime == fp1Time):
                    print("Posting a Free Practice discussion thread")
                    post = postToSubreddit(subreddit, weekend, "Free Practice", live=False)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a Free Practice discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice", css_class="practice")
                    print("Posting a FP1 live thread")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 1", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a FP1 live discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP1 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 1", css_class="practice")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.1): {}".format(e))
            try:
                if fp2Time < currentTime and (prevTime < fp2Time or prevTime == fp2Time):
                    print("Posting a FP2 live thread")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 2", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a FP2 discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP2 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 2", css_class="practice")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.2): {}".format(e))
            try:
                if fp3Time < currentTime and (prevTime < fp3Time or prevTime == fp3Time):
                    print("Posting a FP3 discussion")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 3", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a FP3 discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP3 ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Free Practice 3", css_class="practice")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.3): {}".format(e))
            try:
                if qualiTime < currentTime and (prevTime < qualiTime or prevTime == qualiTime):
                    print("Posting a qualifying discussion")
                    post = postToSubreddit(subreddit, weekend, "Qualifying")
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a qualifying discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "Q ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Qualifying", css_class="qualifying")
                    print("Posting a qualifying live thread")
                    post = postToSubreddit(subreddit, weekend, "Qualifying", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a qualifying live thread")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "Q ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Qualifying", css_class="qualifying")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.4): {}".format(e))
            try:
                if preraceTime < currentTime and (prevTime < preraceTime or prevTime == preraceTime):
                    print("Posting a race discussion")
                    post = postToSubreddit(subreddit, weekend, "Race")
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=False)
                    print("Successfully posted a race discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "Race ^D")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Race", css_class="race")
                    print("Posting a race live thread")
                    post = postToSubreddit(subreddit, weekend, "Race", live=True)
                    if not settings["testingMode"]:
                        post.mod.sticky(bottom=True)
                    print("Successfully posted a race live thread")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "Race ^L")
                    print("Successfully updated the top bar")
                    post.mod.flair(text="Race", css_class="race")
                    post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 2.5): {}".format(e))
                
        else:
            try:
                if fp1Time < currentTime and (prevTime < fp1Time or prevTime == fp1Time):
                    print("Posting a FP1 discussion")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 1")
                    print("Successfully posted a FP1 discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP1")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 1", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.1): {}".format(e))
            try:
                if fp2Time < currentTime and (prevTime < fp2Time or prevTime == fp2Time):
                    print("Posting a FP2 discussion")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 2")
                    print("Successfully posted a FP2 discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP2")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 2", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.2): {}".format(e))
            try:
                if fp3Time < currentTime and (prevTime < fp3Time or prevTime == fp3Time):
                    print("Posting a FP3 discussion")
                    post = postToSubreddit(subreddit, weekend, "Free Practice 3")
                    print("Successfully posted a FP3 discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "FP3")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Free Practice 3", css_class="practice")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.3): {}".format(e))
            try:
                if qualiTime < currentTime and (prevTime < qualiTime or prevTime == qualiTime):
                    print("Posting a qualifying discussion")
                    post = postToSubreddit(subreddit, weekend, "Qualifying")
                    print("Successfully posted a qualifying discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "Q")
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
                    post = postToSubreddit(subreddit, weekend, "Pre Race")
                    print("Successfully posted a pre-race discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "PR")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Pre Race", css_class="race")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.5): {}".format(e))
            try:
                if raceTime < currentTime and (prevTime < raceTime or prevTime == raceTime):
                    print("Posting a race discussion")
                    post = postToSubreddit(subreddit, weekend, "Race", fc)
                    print("Successfully posted a race discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "R")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    post.mod.flair(text="Race", css_class="race")
                    if settings["suggestedNew"]:
                        post.mod.suggested_sort(sort="new")
            except Exception as e:
                print("Error in scheduleChecker (flag 3.6): {}".format(e))
        try:
            if updateTime < currentTime and (prevTime < updateTime or prevTime == updateTime):
                print("Updating the sidebar")
                race = updateSidebarInfo(subreddit)
                if race == False:
                    print("The bot failed while updating the information in the sidebar.")
                else:
                    print("Updating the information in the F1 sidebar for the {}".format(race))
        except Exception as e:
            print("Error in scheduleChecker (flag 4): {}".format(e))
        try:
            if weekend.dadTime < currentTime and (prevTime < weekend.dadTime or prevTime == weekend.dadTime):
                print("Posting a day-after-debrief discussion")
                post = postToSubreddit(subreddit, weekend, "Day after Debrief")
                if settings["newFormat"]:
                    post.mod.sticky(bottom=False)
                print("Successfully posted a day-after-debrief discussion")
                print("Updating top bar")
                updateTopBar(subreddit, post, weekend, "DaD")
                print("Successfully updated the top bar")
                post.mod.flair(text="Day after Debrief", css_class="feature")
        except Exception as e:
            print("Error in scheduleChecker (flag 5): {}".format(e))
        for i in range(len(twitterTimes)):
            events = ["Free Practice 1 for the {} Grand Prix".format(weekend.namean), "Free Practice 2 for the {} Grand Prix".format(weekend.namean), "Free Practice 3 for the {} Grand Prix".format(weekend.namean), "Qualifying for the {} Grand Prix".format(weekend.namean), "The {} Grand Prix".format(weekend.namean)]
            try:
                if twitterTimes[i] < currentTime and (prevTime < twitterTimes[i] or prevTime == twitterTimes[i]):
                    print("Posting a tweet")
                    if not settings["testingMode"]:
                        tweet = twitter.update_status("Reminder: {0} starts in one hour. #{1}GP".format(events[i], weekend.namean.replace(" ", "")))
                    print("Successfully posted a tweet")
            except Exception as e:
                print("Error in scheduleChecker (flag 6): {}".format(e))
    for techDate in weekends.techTalks:
        try:
            if techDate < currentTime and (prevTime < techDate or prevTime == techDate):
                print("Posting a Tech Talk thread")
                title = "Tech Talk {}".format(weekdayToFullWord(techDate.weekday()))
                content = content = "### Welcome to the Tech Talk {0}!\n\nIn this weekly thread, we'd like to give you all a place to discuss technical aspects of the sport. Discussion topics could include characteristics of the cars; recent or planned aero, chassis, engine, and tyre developments; analysis of images; and model-based or data-based predictions. We hope that this will promote more detailed technical discussions in the subreddit.\n\nLow effort comments, such as memes and jokes will be deleted, as will off-topic content, such as discussions centered on drivers. We also discourage superficial comments that contain no analysis or reasoning in this thread.\n\n#### Interesting links\n\nBe sure to check our /r/F1Technical for more in-depth analysis.".format(weekdayToFullWord(techDate.weekday()))
                post = subreddit.submit(title, content, send_replies=False)
                try:
                    checkPost = subreddit.sticky(number=2)
                    subreddit.sticky(number=1).mod.sticky(state=False)
                except Exception as e:
                    print("Error while removing top sticky in scheduleChecker: {}".format(e))
                post.mod.sticky()
                print("Successfully posted a tech talk discussion")
                post.mod.flair(text="Tech Talk", css_class="feature")
        except Exception as e:
            print("Error in scheduleChecker (flag 7): {}".format(e))

def updateSidebarInfo(subreddit):
    try:
        print("Updating the info in the F1 sidebar")
        beginMarkerHead = "[](/beginInfoHead)"
        endMarkerHead = "[](/endInfoHead)"
        beginMarkerSched = "[](/beginInfoSched)"
        endMarkerSched = "[](/endInfoSched)"
        beginMarkerCirc = "[](/beginInfoCirc)"
        endMarkerCirc = "[](/endInfoCirc)"
        beginMarkerLast = "[](/beginInfoLast)"
        endMarkerLast = "[](/endInfoLast)"
        beginMarkerTrack = "[](/beginTrackname)"
        endMarkerTrack = "[](/endTrackname)"
        beginMarkerDriver = "[](/beginDriverStand)"
        endMarkerDriver = "[](/endDriverStand)"
        beginMarkerTeam = "[](/beginTeamStand)"
        endMarkerTeam = "[](/endTeamStand)"
        oldSidebar = subreddit.mod.settings()["description"]
        startIndexHead = oldSidebar.find(beginMarkerHead)+len(beginMarkerHead)
        endIndexHead = oldSidebar.find(endMarkerHead)
        startIndexSched = oldSidebar.find(beginMarkerSched)+len(beginMarkerSched)
        endIndexSched = oldSidebar.find(endMarkerSched)
        startIndexCirc = oldSidebar.find(beginMarkerCirc)+len(beginMarkerCirc)
        endIndexCirc = oldSidebar.find(endMarkerCirc)
        startIndexLast = oldSidebar.find(beginMarkerLast)+len(beginMarkerLast)
        endIndexLast = oldSidebar.find(endMarkerLast)
        w = nextDate()
        if startIndexHead == -1 or endIndexHead == -1 or startIndexSched == -1 or endIndexSched == -1 or startIndexCirc == -1 or endIndexCirc == -1 or startIndexLast == -1 or endIndexLast == -1:
            return False
        else:
            infoHead = "{0} Grand Prix\n - {1}, {2}".format(w.namean, w.city, w.country)
            infoSched = "\n>|Session | Time (UTC)\n|-|-\nFree Practice 1|{0} • {1:02d}:{2:02d}\nFree Practice 2|{3} • {4:02d}:{5:02d}\nFree Practice 3|{6} • {7:02d}:{8:02d}\nQualifying|{9} • {10:02d}:{11:02d}\nRace|{12} • {13:02d}:{14:02d}".format(weekdayToWord(w.fp1Time.weekday()), w.fp1Time.hour, w.fp1Time.minute, weekdayToWord(w.fp2Time.weekday()), w.fp2Time.hour, w.fp2Time.minute, weekdayToWord(w.fp3Time.weekday()), w.fp3Time.hour, w.fp3Time.minute, weekdayToWord(w.qualiTime.weekday()), w.qualiTime.hour, w.qualiTime.minute, weekdayToWord(w.raceTime.weekday()), w.raceTime.hour, w.raceTime.minute)
            infoCirc = "{0}\n>\n|||\n|-|-\nLaps|{1}\n|Circuit Length|{2} km ({3:.3f} mi)\nRace Length|{4} ({5:.3f} mi)\nFirst Held|{6}\nLap Record|{7} ([]({8}) {9}, {10}, {11})\nLinks|[Track Guide]({12}) - [Wikipedia]({13})".format(w.circuit, w.laps, w.length, w.length*0.62137, w.distance, w.distance*0.62137, w.firstHeld, w.lapRecordTime, w.lapRecordFlag, abbrevName(w.lapRecordHolder), w.lapRecordTeam, w.lapRecordYear, w.linkF1, w.linkWikiRace)
            infoLast = "\n[]({0}) {1}, {2}, {3}\n> #Podium\n[]({4}) {5}, {6}\n> \n[]({7}) {8}, {9}, {10}\n> \n[]({11}) {12}, {13}, {14}\n> \n#Fastest Lap\n[]({15}) {16}, {17}, {18}".format(w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.prevYearWinnerFlag, abbrevName(w.prevYearWinner), w.prevYearWinnerTeam, w.prevYearSecondFlag, abbrevName(w.prevYearSecond), w.prevYearSecondTeam, w.prevYearSecondDelta, w.prevYearThirdFlag, abbrevName(w.prevYearThird), w.prevYearThirdTeam, w.prevYearThirdDelta, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime)
            newSidebar = oldSidebar[:startIndexHead]+infoHead+oldSidebar[endIndexHead:startIndexSched]+infoSched+oldSidebar[endIndexSched:startIndexCirc]+infoCirc+oldSidebar[endIndexCirc:startIndexLast]+infoLast+oldSidebar[endIndexLast:]
            try:
                subreddit.stylesheet.upload("race-pic", "img/{}-1.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 1: {}".format(e))
            try:
                subreddit.stylesheet.upload("race-pic-2", "img/{}-2.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 2: {}".format(e))
            try:
                subreddit.stylesheet.upload("race-pic-3", "img/{}-3.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 3: {}".format(e))
            try:
                subreddit.stylesheet.upload("circuit-map", "img/{}-circuit.png".format(w.country.lower().replace(" ", "")))
                startIndexTrack = newSidebar.find(beginMarkerTrack)+len(beginMarkerTrack)
                endIndexTrack = newSidebar.find(endMarkerTrack)
                if startIndexTrack != -1 and endIndexTrack != -1:
                    newSidebar = newSidebar[:startIndexTrack]+w.circuit+newSidebar[endIndexTrack:]
            except Exception as e:
                print("Failed to upload circuit map: {}".format(e))
            try:
                subreddit.stylesheet.update(subreddit.stylesheet().stylesheet, reason="Updating race pics and circuit map")
            except Exception as e:
                print("Failed to update stylesheet: {}".format(e))
            try:
                driverStand = ws.driverStandings()
                teamStand = ws.teamStandings()
                if driverStand and teamStand:
                    startIndexDriver = newSidebar.find(beginMarkerDriver)+len(beginMarkerDriver)
                    endIndexDriver = newSidebar.find(endMarkerDriver)
                    startIndexTeam = newSidebar.find(beginMarkerTeam)+len(beginMarkerTeam)
                    endIndexTeam = newSidebar.find(endMarkerTeam)
                    if startIndexDriver != -1 and endIndexDriver != -1 and startIndexTeam != -1 and endIndexTeam != -1:
                        newSidebar = newSidebar[:startIndexDriver]+driverStand+newSidebar[endIndexDriver:startIndexTeam]+teamStand+newSidebar[endIndexTeam:]
            except Exception as e:
                print("Failed to update driver and team standings: {}".format(e))
            subreddit.mod.update(description=newSidebar)
            print("Successfully updated the info in the sidebar")
            return "{} Grand Prix".format(w.namean)
    except Exception as e:
        print("Error in updateSidebarInfo: {}".format(e))

def checkMail(subreddit, private_subreddit, formula1exp, forecast):
    #Checks mailbox
    global lastCommand
    global lastAlert
    global qualiResultTime
    global raceResultTime
    print("Checking mail")
    messages = r.inbox.unread()
    counter = 0
    try:
        for message in messages:
            print("Reading a message from {0}: {1}".format(message.author, message.body))
            message.mark_read()
            counter += 1
            if message.author in moderators and message.body.lower() == "post":
                for weekend in weekends.allWeekends:
                    try:
                        if weekend.qualiTime < currentTime and currentTime < weekend.raceTime:
                            if lastCommand != [weekend.country, "quali"]:
                                print("Posting a post-quali discussion")
                                if not settings["testingMode"]:
                                    post = postToSubreddit(subreddit, weekend, "Post Qualifying")
                                else:
                                    post = postToSubreddit(formula1exp, weekend, "Post Qualifying")
                                qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                                print("Successfully posted a post-qualifying discussion")
                                print("Updating top bar")
                                updateTopBar(subreddit, post, weekend, "PQ")
                                print("Successfully updated the top bar")
                                addToHub(post, weekend)
                                message.reply("Successfully posted a post-qualifying discussion\n\n{}".format(post.shortlink))
                                lastCommand = [weekend.country, "quali"]
                                if settings["suggestedNew"]:
                                    setSuggestedSort("qualifying", "blank")
                                post.mod.flair(text="Post Qualifying", css_class="post-qualifying")
                            else:
                                message.reply("Somebody else already posted a post-qualifying discussion")
                    except Exception as e:
                        print("Error in checkMail (flag 1): {}".format(e))
                    try:
                        if weekend.raceTime < currentTime and currentTime < weekend.dadTime:
                            if lastCommand != [weekend.country, "race"]:
                                print("Posting a post-race discussion")
                                if not settings["testingMode"]:
                                    post = postToSubreddit(subreddit, weekend, "Post Race")
                                else:
                                    post = postToSubreddit(formula1exp, weekend, "Post Race")
                                raceResultTime = currentTime+datetime.timedelta(minutes=1)
                                print("Successfully posted a post-race discussion")
                                print("Updating top bar")
                                updateTopBar(subreddit, post, weekend, "PR")
                                print("Successfully updated the top bar")
                                addToHub(post, weekend)
                                message.reply("Successfully posted a post-race discussion\n\n{}".format(post.shortlink))
                                lastCommand = [weekend.country, "race"]
                                if settings["suggestedNew"]:
                                    setSuggestedSort("race", "blank")
                                post.mod.flair(text="Post Race", css_class="post-race")
                            else:
                                message.reply("Somebody else already posted a post-race discussion")
                    except Exception as e:
                        print("Error in checkMail (flag 2): {}".format(e))
            if message.author in moderators and message.body.lower() == "weather":
                fc = updateWeatherPrediction(subreddit, forecast)
                if fc == False:
                    message.reply("Something went wrong while updating the weather prediction")
                else:
                    message.reply("Successfully updated the weather prediction\n\n/r/formula1")
            if message.author in moderators and message.body.lower() == "clear failsafe":
                message.reply("Successfully cleared the failsafe")
                lastCommand = [1, 1]
            if message.author in moderators and message.body.lower() == "sidebar":
                race = updateSidebarInfo(subreddit)
                if race == False:
                    message.reply("The bot failed while updating the information in the sidebar.")
                else:
                    message.reply("Updating the information in the F1 sidebar for the {}".format(race))
            if message.author in moderators and message.body.lower() == "results":
                message.reply(ws.driverStandings())
            if message.author in moderators and message.body.lower() == "grid":
                message.reply(ws.startingGrid(prevDate()))
            if message.author in moderators and message.body.lower() == "qualiresults":
                success = postResults("qualifying")
                if success:
                    message.reply("Successfully posted the qualifying results")
                else:
                    message.reply("Could not post the qualifying results")
            if message.author in moderators and message.body.lower() == "raceresults":
                success = postResults("race")
                if success:
                    message.reply("Successfully posted the race results")
                else:
                    message.reply("Could not post the race results")
            if message.author in moderators and message.body.lower() == "finished":
                finished = checkSessionFinished(subreddit, "any")
                if not finished:
                    message.reply("Session has not finished yet.")
            if message.author in moderators and message.body.lower() == "flairs":
                if alertState == "normal":
                    updateFlairCounts(subreddit, message.author)
                    message.reply("Successfully updated the flair counts.\n\n/r/{}/wiki/flaircounts".format(subreddit.display_name))
                else:
                    message.reply("F1-Bot is currently occupied with the current qualifying/race. Please try again later.")
            if (message.author in moderators or message.author in authorized) and message.body.lower() == "traffic":
                trafficReport = getTrafficReport(subreddit)
                if trafficReport:
                    message.reply(trafficReport)
                else:
                    message.reply("Something went wrong while generating a traffic report. Please contact /u/Redbiertje.")
            if counter == 5+25*(alertState=="normal") and lastAlert + datetime.timedelta(minutes=10) < currentTime:
                lastAlert = currentTime
                print("Alerting mod team of inbox overload")
                subreddit.message("F1-Bot: Overload alert", "This is an automated message to let you know that the bot's inbox is being flooded. Please take the following steps:\n\n1. Make sure that all recent posts by /u/F1-Bot have the inbox replies setting disabled.\n2. Open /u/F1-Bot's inbox, and mark all messages as read.")
    except Exception as e:
        print("Error in checkMail: {}".format(e))
    if settings["readRobust"]:
        print("Reading /r/formula1bot posts as mail")
        try:
            posts = private_subreddit.new(limit=5)
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
                                        submittedpost = postToSubreddit(subreddit, weekend, "Post Qualifying")
                                        submittedpost.mod.sticky(bottom=False)
                                        qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                                        print("Successfully posted a post-qualifying discussion")
                                        print("Updating top bar")
                                        updateTopBar(subreddit, submittedpost, weekend, "PQ")
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
                                        submittedpost = postToSubreddit(subreddit, weekend, "Post Race")
                                        submittedpost.mod.sticky(bottom=False)
                                        raceResultTime = currentTime+datetime.timedelta(minutes=1)
                                        print("Successfully posted a post-race discussion")
                                        print("Updating top bar")
                                        updateTopBar(subreddit, submittedpost, weekend, "PR")
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
                        fc = updateWeatherPrediction(subreddit, forecast)
                        if fc == False:
                            post.reply("Something went wrong while updating the weather prediction")
                        else:
                            post.reply("Successfully updated the weather prediction\n\n/r/formula1")
                    if postMessage.lower() == "clear failsafe":
                        post.reply("Successfully cleared the failsafe")
                        lastCommand = [1, 1]
                    if postMessage.lower() == "sidebar":
                        race = updateSidebarInfo(subreddit)
                        if race == False:
                            post.reply("The bot failed while updating the information in the sidebar.")
                        else:
                            post.reply("Updating the information in the F1 sidebar for the {}".format(race))
        except Exception as e:
            print("Error in robust checkMail: {}".format(e))
    print("Finished checking mail")
    
def checkSessionFinished(subreddit, session):
    global lastCommand
    global lastQ2Time
    global qualiResultTime
    global raceResultTime
    try:
        print("Checking if the session is finished")
        if session == "quali":
            weekends = [nextDate()]
        elif session == "race":
            weekends = [prevDate()]
        else:
            weekends = [prevDate(), nextDate()]
        for weekend in weekends:
            if weekend.qualiTime < currentTime and currentTime < weekend.raceTime and lastCommand != [weekend.country, session]:
                if ws.sessionFinished(session) and settings["autoPost"] and lastQ2Time+datetime.timedelta(minutes=2) < currentTime:
                    print("Posting a post-quali discussion")
                    if not settings["testingMode"]:
                        post = postToSubreddit(subreddit, weekend, "Post Qualifying")
                    else:
                        post = postToSubreddit(formula1exp, weekend, "Post Qualifying")
                    qualiResultTime = currentTime+datetime.timedelta(minutes=1)
                    print("Successfully posted a post-qualifying discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "PQ")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    lastCommand = [weekend.country, "quali"]
                    if settings["suggestedNew"]:
                        setSuggestedSort("qualifying", "blank")
                    post.mod.flair(text="Post Qualifying", css_class="post-qualifying")
                    return True
            if weekend.raceTime < currentTime and currentTime < weekend.dadTime and lastCommand != [weekend.country, session]:
                if ws.sessionFinished(session) and settings["autoPost"]:
                    print("Posting a post-race discussion")
                    if not settings["testingMode"]:
                        post = postToSubreddit(subreddit, weekend, "Post Race")
                    else:
                        post = postToSubreddit(formula1exp, weekend, "Post Race")
                    raceResultTime = currentTime+datetime.timedelta(minutes=1)
                    print("Successfully posted a post-race discussion")
                    print("Updating top bar")
                    updateTopBar(subreddit, post, weekend, "PR")
                    print("Successfully updated the top bar")
                    addToHub(post, weekend)
                    lastCommand = [weekend.country, "race"]
                    if settings["suggestedNew"]:
                        setSuggestedSort("race", "blank")
                    post.mod.flair(text="Post Race", css_class="post-race")
                    return True
        return False
    except Exception as e:
        print("Error in checkSessionFinished: {}".format(e))
        return False

def botState():
    #Defines the state of the bot
    for weekend in weekends.allWeekends:
        if weekend.qualiTime < currentTime and currentTime < weekend.qualiTime + datetime.timedelta(hours=1, minutes=30) and lastCommand != [weekend.country, "quali"]:
            return "quali"
        elif weekend.raceTime < currentTime and currentTime < weekend.raceTime + datetime.timedelta(hours=2, minutes=30) and lastCommand != [weekend.country, "race"]:
            return "race"
    return "normal"

def updateWeatherPrediction(subreddit, forecast):
    #Updates the weather prediction in the sidebar of the subreddit
    print("Updating the weather prediction")
    beginMarker = "[](/weatherBegin)"
    endMarker = "[](/weatherEnd)"
    nextWeekend = nextDate()
    fp1Time = nextWeekend.fp1Time
    fp2Time = nextWeekend.fp2Time
    fp3Time = nextWeekend.fp3Time
    qualiTime = nextWeekend.qualiTime
    raceTime = nextWeekend.raceTime
    try:
        fc = getForecast()
        if fc == False:
            fc = forecast
        oldSidebar = subreddit.mod.settings()["description"]
        startIndex = oldSidebar.find(beginMarker)+len(beginMarker)
        endIndex = oldSidebar.find(endMarker)
        if startIndex == -1 or endIndex == -1:
            return False
        elif raceTime - datetime.timedelta(days=4, hours=12, minutes=10) < currentTime:
            try:
                fp1Status = fc.get_weather_at(fp1Time)
            except:
                fp1Status = 0
            try:
                fp2Status = fc.get_weather_at(fp2Time)
            except:
                fp2Status = 0
            try:
                fp3Status = fc.get_weather_at(fp3Time)
            except:
                fp3Status = 0
            try:
                qualiStatus = fc.get_weather_at(qualiTime)
            except:
                qualiStatus = 0
            try:
                raceStatus = fc.get_weather_at(raceTime)
            except:
                raceStatus = 0
            statusList = [fp1Status, fp2Status, fp3Status, qualiStatus, raceStatus]
            abbrev = ["Free Practice 1", "Free Practice 2", "Free Practice 3", "Qualifying", "Race"]
            prediction = "Weather Prediction"
            for i in range(len(statusList)):
                if statusList[i] != 0:
                    prediction += "\n> - {0}\n>  - []({1})\n>  - {2}\n>  - {3} °C / {4} °F".format(abbrev[i], weatherIcon(statusList[i].get_weather_icon_name()), weatherChange(firstCaps(statusList[i].get_detailed_status())), int(statusList[i].get_temperature(unit="celsius")["temp"]), int(statusList[i].get_temperature(unit="fahrenheit")["temp"]))
            prediction += "\n>\n> [Link to source](http://openweathermap.org/city/{})".format(nextWeekend.weatherID)
            newSidebar = oldSidebar[:startIndex]+prediction+oldSidebar[endIndex:]
            subreddit.mod.update(description=newSidebar)
        else:
            newSidebar = oldSidebar[:startIndex]+"Weather Prediction\n> The weather prediction is not yet available."+oldSidebar[endIndex:]
            subreddit.mod.update(description=newSidebar)
        print("Sucessfully updated the sidebar")
        return fc
    except Exception as e:
        print("Error in updateWeatherPrediction: {}".format(e))
        return False

def checkAll(subreddit):
    #Checks /r/all to see if there are any posts from /r/formula1. Any posts from /r/formula1 in /r/all will receive a flair
    all = r.subreddit("all")
    for submission in all.hot(limit=50):
        if submission.subreddit.display_name == subreddit.display_name and submission.link_flair_css_class != "sub-all":
            print("Found a new post in /r/all!")
            try:
                if submission.link_flair_text != None:
                    submission.mod.flair(text="{} /r/all".format(submission.link_flair_text), css_class="sub-all")
                else:
                    submission.mod.flair(text="/r/all", css_class="sub-all")
            except Exception as e:
                print("Error in checkAll: {}".format(e))
        
def getForecast():
    #Retrieves a weather forecast from the weather API
    print("Retrieving weather prediction")
    nextWeekend = nextDate()
    try:
        fc = owm.three_hours_forecast_at_id(nextWeekend.weatherID)
        print("Successfully retrieved weather forecast for {}".format(nextWeekend.city))
        return fc
    except Exception as e:
        print("Error in getForecast: {}".format(e))
        return False
        
def protectInbox():
    #Unused function to protect the inbox from overflowing
    try:
        lastPosts = r.user.me().submissions.new(limit=10)
        for post in lastPosts:
            post.disable_inbox_replies()
    except Exception as e:
        print("Error in protectInbox: {}".format(e))
        return False

def postResults(session):
    try:
        print("Attempting to post results")
        if session == "qualifying":
            weekend = nextDate()
            for oldPost in r.user.me().new(limit=5):
                if oldPost.title == "{0} {1} Grand Prix - Post Qualifying Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    content = oldPost.selftext
                    marker = "[](/results)"
                    results = ws.qualiResults(weekend)
                    if results:
                        newContent = content.replace(marker, "---\n\n"+results)
                        oldPost.edit(newContent)
                        print("Successfully posted qualifying results")
                        return True
                    else:
                        return False
        if session == "race":
            weekend = prevDate()
            for oldPost in r.user.me().new(limit=5):
                if oldPost.title == "{0} {1} Grand Prix - Post Race Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    content = oldPost.selftext
                    marker = "[](/results)"
                    indexMarker = content.find(marker)
                    results = ws.raceResults(weekend)
                    if results:
                        newContent = content.replace(marker, "---\n\n"+results)
                        oldPost.edit(newContent)
                        print("Successfully posted race results")
                        return True
                    else:
                        return False
    except Exception as e:
        print("Error in postResults: {}".format(e))
        
def addToHub(post, weekend):
    beginMarker = "[](/sessionsBegin)"
    endMarker = "[](/sessionsEnd)"
    try:
        print("Adding post to Weekend Hub")
        for oldPost in r.user.me().new(limit=15):
            if oldPost.title == "{0} {1} Grand Prix - Weekend Hub".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                content = oldPost.selftext
                beginIndex = content.find(beginMarker)+len(beginMarker)
                endIndex = content.find(endMarker)
                if beginIndex == -1 or endIndex == -1:
                    return False
                elif post.title == "{0} {1} Grand Prix - Free Practice 1 Discussion".format(currentYear, weekend.namean):
                    newContent = content[:beginIndex]+"\n\n - [{0}]({1})".format(post.title.split("-")[1].lstrip(), post.permalink)+content[endIndex:]
                else:
                    newContent = content[:endIndex]+"\n - [{0}]({1})".format(post.title.split("-")[1].lstrip(), post.permalink)+content[endIndex:]
                oldPost.edit(newContent)
                print("Successfully added post to Weekend Hub")
                return True
    except Exception as e:
        print("Error in addToHub: {}".format(e))
        return False
    

def setSuggestedSort(session, sorting):
    try:
        print("Setting the suggested sort to {}".format(sorting))
        if sorting not in ["confidence", "top", "new", "controversial", "old", "random", "qa", "blank"]:
            print("Error in setSuggestedSort: Invalid sorting given.")
            return False
        if session == "qualifying":
            weekend = nextDate()
            for oldPost in r.user.me().new(limit=5):
                if oldPost.title == "{0} {1} Grand Prix - Qualifying Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    oldPost.mod.suggested_sort(sort=sorting)
                    return True
        if session == "race":
            weekend = prevDate()
            for oldPost in r.user.me().new(limit=5):
                if oldPost.title == "{0} {1} Grand Prix - Race Discussion".format(currentYear, weekend.namean) and oldPost.subreddit == "formula1":
                    oldPost.mod.suggested_sort(sort=sorting)
                    return True
    except Exception as e:
        print("Error in setSuggestedSort: {}".format(e))
        
def getSettings(subreddit):
    try:
        settings = {}
        defaultSettings = {"replaceSticky": True, "testingMode": False, "readRobust": True, "suggestedNew": False, "newFormat": True, "dailyTweet": True, "scoreThreshold": 1000, "autoPost": True}
        print("Pulling bot settings from the wiki")
        wikiContent = subreddit.wiki['botsettings'].content_md
        wikiRows = wikiContent.split("\r\n")
        for row in wikiRows:
            if row != "":
                setting, value = tuple(row.replace(" ", "").split("#")[0].split("="))
                if value == "True" or value == "true":
                    settings[setting] = True
                if value == "False" or value == "false":
                    settings[setting] = False
                if value.isdigit():
                    settings[setting] = int(value)
        if sorted(settings.keys()) == sorted(defaultSettings.keys()):
            return settings
        else:
            return defaultSettings
    except Exception as e:
        print("Error in pullSettings: {}".format(e))
        return False
        
def updateFlairCounts(subreddit, redditor):
    try:
        t_start = time.time()
        flairs = {}
        for flair in subreddit.flair(limit=None):
            flairName = flair['flair_css_class']
            if flairName not in flairs:
                flairs[flairName] = 0
            flairs[flairName] += 1
        sorted_flairs = sorted(flairs.items(), key=lambda x: x[1], reverse=True)
        wikiPage = subreddit.wiki['flaircounts']
        content = "# Formula 1 flair counts\n\n**[Click here to update the flair counts](https://www.reddit.com/message/compose?to=F1-Bot&subject=command&message=flairs)**\n\nLast update: {0} {1} {2}, {3:02d}:{4:02d}\n\n---\n\n## Flair counts\n\n|CSS class|Count|\n|--:|:--|".format(currentTime.day, monthToWord(currentTime.month), currentTime.year, currentTime.hour, currentTime.minute)
        for CSS, count in sorted_flairs:
            content += "\n|{0}|{1}|".format(CSS, count)
        wikiPage.edit(content, reason="{} requested an update.".format(redditor))
    except Exception as e:
        print("Error in updateFlairCounts: {}".format(e))
                
def tweetTopPost(subreddit):
    try:
        print("Tweeting top post of the day")
        topPosts = subreddit.top("day", limit=1)
        for topPost in topPosts:
            break
        if topPost.score >= settings["scoreThreshold"]:
            wikiContent = subreddit.wiki['tweettemplates'].content_md
            templates = [line[1:].lstrip() for line in wikiContent.split("---")[1].lstrip().rstrip().split("\r\n")]
            selectedTemplate = random.choice(templates)
            tweetText = selectedTemplate.replace("<link>", topPost.shortlink).replace("<score>", str(topPost.score)).replace("<user>", "/u/"+topPost.author.name)
            try:
                if not settings["testingMode"]:
                    tweet = twitter.update_status(tweetText)
                    print("Successfully posted a tweet")
            except Exception as e:
                print("Error in tweetTopPost (Twitter section): {}".format(e))
    except Exception as e:
        print("Error in checkTopPost: {}".format(e))
        
def getTrafficReport(subreddit):
    try:
        traffic_dict = subreddit.traffic()
        day_stats = traffic_dict['day']
        hour_stats = traffic_dict['hour']
        month_stats = traffic_dict['month']
        report = "#Traffic stats for /r/formula1\n\nGenerated on {0} {1} {2}, {3:02d}:{4:02d}\n\nAll times in UTC\n\n##Traffic by day\n\n|Date|Unique users|Total page views|Subscribes|\n|:--|:--|:--|:--|".format(currentTime.day, monthToWord(currentTime.month), currentTime.year, currentTime.hour, currentTime.minute)
        for timestamp, uniques, pageviews, subs in day_stats:
            date = datetime.datetime.fromtimestamp(timestamp)
            dateString = "{0} {1} {2}".format(date.year, monthToWord(date.month), date.day)
            if pageviews != 0:
                report += "\n|{0}|{1}|{2}|{3}|".format(dateString, uniques, pageviews, subs)
        report += "\n\n##Traffic by hour\n\n|Date|Unique users|Total page views|\n|:--|:--|:--|"
        for timestamp, uniques, pageviews in hour_stats:
            date = datetime.datetime.fromtimestamp(timestamp)
            dateString = "{0} {1}, {2:02d}:00".format(monthToWord(date.month), date.day, date.hour)
            if pageviews != 0:
                report += "\n|{0}|{1}|{2}|".format(dateString, uniques, pageviews)
        report += "\n\n##Traffic by month\n\n|Date|Unique users|Total page views|\n|:--|:--|:--|"
        for timestamp, uniques, pageviews in month_stats:
            date = datetime.datetime.fromtimestamp(timestamp)
            dateString = "{0} {1}".format(date.year, monthToWord(date.month))
            if pageviews != 0:
                report += "\n|{0}|{1}|{2}|".format(dateString, uniques, pageviews)
        report += "\n\nRaw dictionary:\n\n    {}".format(traffic_dict)
        return report
    except Exception as e:
        print("Error in getTrafficReport: {}".format(e))
        return False
    
alertState = botState()
settings = getSettings(subreddit)
print("Current bot state: {}".format(alertState))
if boot == True:
    boot = False
    forecast = getForecast()
if currentTime.hour != prevTime.hour:
    forecast = updateWeatherPrediction(subreddit, forecast)
if currentTime.hour == 15 and prevTime.hour == 14 and settings["dailyTweet"]:
    tweetTopPost(subreddit)
if int(currentTime.minute/10) != int(prevTime.minute/10):
    pass
    #checkAll(subreddit)
if raceResultTime < currentTime and (prevTime < raceResultTime or prevTime == raceResultTime):
    weekend = prevDate()
    success = postResults("race")
    if not success and raceResultTime < weekend.raceTime + datetime.timedelta(hours=6):
        raceResultTime += datetime.timedelta(minutes=1)
if qualiResultTime < currentTime and (prevTime < qualiResultTime or prevTime == qualiResultTime):
    weekend = nextDate()
    success = postResults("qualifying")
    if not success and weekend.raceTime < qualiResultTime + datetime.timedelta(days=2):
        qualiResultTime += datetime.timedelta(minutes=1)
if alertState == "normal":
    updateCountdown(subreddit)
    if settings["testingMode"]:
        scheduleChecker(formula1exp, forecast)
    else:
        scheduleChecker(subreddit, forecast)
    checkMail(subreddit, private_subreddit, formula1exp, forecast)
    prevTime = currentTime
    time.sleep(30)
elif alertState == "quali" or alertState == "race":
    updateCountdown(subreddit)
    if settings["testingMode"]:
        scheduleChecker(formula1exp, forecast)
    else:
        scheduleChecker(subreddit, forecast)
    checkMail(subreddit, private_subreddit, formula1exp, forecast)
    checkSessionFinished(subreddit, alertState)
    prevTime = currentTime
    for i in range(4):
        checkMail(subreddit, private_subreddit, formula1exp, forecast)
        checkSessionFinished(subreddit, alertState)
    
#Old code that may be VERY useful some day
#
#Old session template
#content = "### ROUND {0}: {1} []({2})\n\n|{3}|\n|:-:|\n|{4} {5} {6} - {7} {8} {9}|\n|{10}|\n\n| Session | UTC |\n| - | - |\n| Free Practice 1 | {42} |\n| Free Practice 2 | {43} |\n| Free Practice 3 | {44} |\n| Qualifying | {11} |\n| Race | {12} |\n\n[Click here for start times in your area.](http://f1calendar.com/)\n\n---\n\n#### {13}\n\n**Length:** {14} km ({15:.3f} mi)\n\n**Distance:** {16} laps, {17} km ({18:.3f} mi)\n\n**Lap record:** []({19}) {20}, {21}, {22}, {23}\n\n**{24} pole:** []({25}) {26}, {27}, {28}\n\n**{29} fastest lap:** []({30}) {31}, {32}, {33}\n\n**{34} winner:** []({35}) {36}, {37}\n\n{45}---\n\n####Useful links\n\n- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n- Wiki: [Race]({39}) | [{40}]({41})\n\n---\n\n#### Streaming & Downloads\n\nFor information on streams, please visit /r/MotorSportsStreams. Please do not post information about streams in this thread. Thank you.\n\n---\n\n####Live timing leaderboard\n\nFor those of you who are F1 ACCESS members, you can check the position of the drivers throughout the race on the [official live timing leaderboard](https://www.formula1.com/en/f1-live.html)\n\n---\n\n#### Race Discussion\n\nJoin us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n\nStream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n\nBe sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.".format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
#New session template
#content = "### ROUND {0}: {1} []({2})\n\n|{3}|\n|:-:|\n|{4} {5} {6} - {7} {8} {9}|\n|{10}|\n\n| Session | UTC |\n| - | - |\n| Free Practice 1 | {42} |\n| Free Practice 2 | {43} |\n| Free Practice 3 | {44} |\n| Qualifying | {11} |\n| Race | {12} |\n\n[Click here for start times in your area.](http://f1calendar.com/)\n\n---\n\n#### {13}\n\n**Length:** {14} km ({15:.3f} mi)\n\n**Distance:** {16} laps, {17} km ({18:.3f} mi)\n\n**Lap record:** []({19}) {20}, {21}, {22}, {23}\n\n**{24} pole:** []({25}) {26}, {27}, {28}\n\n**{29} fastest lap:** []({30}) {31}, {32}, {33}\n\n**{34} winner:** []({35}) {36}, {37}\n\n{45}---\n\n####Useful links\n\n- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n- Wiki: [Race]({39}) | [{40}]({41})\n\n---\n\n#### Streaming & Downloads\n\nFor information on streams, please visit /r/MotorSportsStreams. Please do not post information about streams in this thread. Thank you.\n\n---\n\n####Live timing leaderboard\n\nFor those of you who are F1 ACCESS members, you can check the position of the drivers throughout the race on the [official live timing leaderboard](https://www.formula1.com/en/f1-live.html)\n\n---\n\n#### Race Discussion\n\nJoin us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n\nStream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n\nBe sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.".format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
#Post session template
#content = "### ROUND {0}: {1} []({2})\n\n|{3}|\n|:-:|\n|{4} {5} {6} - {7} {8} {9}|\n|{10}|\n\n| Session | UTC |\n| - | - |\n| Free Practice 1 | {42} |\n| Free Practice 2 | {43} |\n| Free Practice 3 | {44} |\n| Qualifying | {11} |\n| Race | {12} |\n\n[Click here for start times in your area.](http://f1calendar.com/)\n\n---\n\n#### {13}\n\n**Length:** {14} km ({15:.3f} mi)\n\n**Distance:** {16} laps, {17} km ({18:.3f} mi)\n\n**Lap record:** []({19}) {20}, {21}, {22}, {23}\n\n**{24} pole:** []({25}) {26}, {27}, {28}\n\n**{29} fastest lap:** []({30}) {31}, {32}, {33}\n\n**{34} winner:** []({35}) {36}, {37}\n\n[](/results)\n\n---\n\n####Useful links\n\n- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n- Wiki: [Race]({39}) | [{40}]({41})\n\n---\n\n#### Streaming & Downloads\n\nFor information on downloads, please visit /r/MotorSportsReplays. Please do not post information about downloads in this thread. Thank you.".format(w.round, w.country, w.flag, w.fullTitle, weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, monthToWord(w.fp1Time.month), weekdayToWord(w.raceTime.weekday()), w.raceTime.day, monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC)
#Day after Debrief
#content = "### ROUND {0}: {1} []({2})\n\n---\n\n####Welcome to the Day after Debrief discussion thread!\n\nNow that the dust has settled in {3}, it's time to calmly discuss the events of the last race weekend. Hopefully, this will foster more detailed and thoughtful discussion than the immediate post race thread now that people have had some time to digest and analyse the results.\n\nLow effort comments, such as memes, jokes, and complaints about broadcasters will be deleted. We also discourage superficial comments that contain no analysis or reasoning in this thread (e.g., 'Great race from X!', 'Another terrible weekend for Y!').\n\nThanks!".format(w.round, w.country, w.flag, w.city)
#Weekend Hub
#content = "### ROUND {0}: {1} []({2})\n\n| Session | UTC | Weather prediction|\n| - | - | - |\n| Free Practice 1 | {3} | []({4}) {5}, {6} °C / {7} °F|\n| Free Practice 2 | {8} | []({9}) {10}, {11} °C / {12} °F|\n| Free Practice 3 | {13} | []({14}) {15}, {16} °C / {17} °F|\n| Qualifying | {18} | []({19}) {20}, {21} °C / {22} °F|\n| Race | {23} | []({24}) {25}, {26} °C / {27} °F|\n\n[Click here](http://f1calendar.com/) for start times in your area.\n\nPlease note that this weather prediction does not get updated. For an up-to-date weather prediction, see the sidebar.\n\n---\n\n#### Threads\n\n**Sessions**\n\n - No links yet\n\n**Extras**\n\n - [/u/Kelly_Johnson's Prediction Competition](https://docs.google.com/forms/d/e/1FAIpQLSfeGdJci-7h5FwDwPr044s400BzqsOJa1tOV8cGBQ3OH6zReg/viewform?usp=sf_link)\n\n####IRC Chat\n\nJoin us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n\nStream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**".format(w.round, w.country, w.flag, fp1UTC, weatherIcon(fp1Status.get_weather_icon_name()), weatherChange(firstCaps(fp1Status.get_detailed_status())), int(fp1Status.get_temperature(unit="celsius")["temp"]), int(fp1Status.get_temperature(unit="fahrenheit")["temp"]), fp2UTC, weatherIcon(fp2Status.get_weather_icon_name()), weatherChange(firstCaps(fp2Status.get_detailed_status())), int(fp2Status.get_temperature(unit="celsius")["temp"]), int(fp2Status.get_temperature(unit="fahrenheit")["temp"]), fp3UTC, weatherIcon(fp3Status.get_weather_icon_name()), weatherChange(firstCaps(fp3Status.get_detailed_status())), int(fp3Status.get_temperature(unit="celsius")["temp"]), int(fp3Status.get_temperature(unit="fahrenheit")["temp"]), qualiUTC, weatherIcon(qualiStatus.get_weather_icon_name()), weatherChange(firstCaps(qualiStatus.get_detailed_status())), int(qualiStatus.get_temperature(unit="celsius")["temp"]), int(qualiStatus.get_temperature(unit="fahrenheit")["temp"]), raceUTC, weatherIcon(raceStatus.get_weather_icon_name()), weatherChange(firstCaps(raceStatus.get_detailed_status())), int(raceStatus.get_temperature(unit="celsius")["temp"]), int(raceStatus.get_temperature(unit="fahrenheit")["temp"]))
