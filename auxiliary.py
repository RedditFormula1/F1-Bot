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
import os
import numpy as np


currentYear = 2020
prevYear = 2019

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
    
def monthToFullWord(i):
    #Turns the number of month of the year into a three-letter string
    months = ["Err", "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
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
    nextWeekend = nextDate()
    try:
        fc = owm.three_hours_forecast_at_id(nextWeekend.weatherID)
        return fc
    except Exception as e:
        print("Error in getForecast: {}".format(e))
        return False

def readlines_reverse(filename):
        """
        Generator for lines of a files reading from the end (for memory purposes)
        """
        with open(filename, errors='ignore') as qfile:
            qfile.seek(0, os.SEEK_END)
            position = qfile.tell()
            line = ''
            while position >= 0:
                qfile.seek(position)
                next_char = qfile.read(1)
                if next_char == "\n":
                    yield line[::-1]
                    line = ''
                else:
                    line += next_char
                position -= 1
            yield line[::-1]

def similarity(d1, d2):
    total = 0
    l1 = np.sqrt(np.sum(np.array(list(d1.values()))**2))
    l2 = np.sqrt(np.sum(np.array(list(d2.values()))**2))
    all_keys = list(set(d1.keys()) | set(d2.keys()))
    for key in all_keys:
        v1 = d1[key]/l1 if key in d1 else 0
        v2 = d2[key]/l2 if key in d2 else 0
        total += v1*v2
    return total
        