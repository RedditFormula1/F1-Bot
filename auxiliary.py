#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
7 May 2019
"""

#Imports
from __future__ import division
import datetime
import sys
import time
import weekends


currentYear = 2019
prevYear = 2018

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
    if string == "N/A":
        return string
    else:
        initial = string.split(' ')[0][0]
        lastname = string.split(' ', 1)[1]
        return "{0}. {1}".format(initial, lastname)

def nextDate():
    #Finds the weekend object of the upcoming race
    currentTime = datetime.datetime.utcnow()
    for weekend in weekends.allWeekends:
        if currentTime < weekend.raceTime:
            return weekend
    return weekends.allWeekends[-1]

def prevDate():
    #Finds the weekend object of the last race
    currentTime = datetime.datetime.utcnow()
    for weekend in weekends.allWeekends[::-1]:
        if weekend.raceTime < currentTime:
            return weekend
    return weekends.allWeekends[0]
    
def getForecast(owm):
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

def getHighlights(raceTime):
    #Uses Pushshift search to find race highlights in past 3 hours
    giffers = ['BottasWMR','Mark4211','pcghx_busch','-acro-','exiledtie', 'buschjp', 'overspeeed']
    currentTime = int(time.time())
    api = PushshiftAPI(r)
    highlights = []
    bodyText = 'Highlight|Thread\n:--|:--\n'\
    for giffer in giffers:
        print('Trying for', giffer)
        for submission in list(api.search_submissions(after=raceTime.timestamp(),
                                    before=currentTime,
                                    subreddit='formula1',
                                    author=giffer,
                                    domain='streamable.com',
                                    filter=['url','author', 'title', 'subreddit'],
                                    limit=150)):
            highlights.append((submission.title, submission.url, submission.permalink, submission.created_utc))
    highlights.sort(key=lambda tup: tup[3])
    for highlight in highlights:
        bodyText = bodyText + f'[{highlight[0]}]({highlight[1]}) | [Link]({highlight[2]}) \n'\

    return bodyText
