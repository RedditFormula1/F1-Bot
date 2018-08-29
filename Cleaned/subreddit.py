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
from sidebar import Sidebar

class Subreddit():

    def __init__(self, sub):
        self.sub = sub
        self.sidebar = Sidebar(self.sub)
    
    def updateFlairCounts(self, redditor)
        try:
            t_start = time.time()
            flairs = {}
            for flair in self.sub.flair(limit=None):
                flairName = flair['flair_css_class']
                if flairName not in flairs:
                    flairs[flairName] = 0
                flairs[flairName] += 1
            sorted_flairs = sorted(flairs.items(), key=lambda x: x[1], reverse=True)
            wikiPage = self.sub.wiki['flaircounts']
            content = "# Formula 1 flair counts\n\n**[Click here to update the flair counts](https://www.reddit.com/message/compose?to=F1-Bot&subject=command&message=flairs)**\n\nLast update: {0} {1} {2}, {3:02d}:{4:02d}\n\n---\n\n## Flair counts\n\n|CSS class|Count|\n|--:|:--|".format(currentTime.day, monthToWord(currentTime.month), currentTime.year, currentTime.hour, currentTime.minute)
            for CSS, count in sorted_flairs:
                content += "\n|{0}|{1}|".format(CSS, count)
            wikiPage.edit(content, reason="{} requested an update.".format(redditor))
        except Exception as e:
            print("Error in updateFlairCounts: {}".format(e))
            
    def postToSubreddit(self, w, thread, fc=False, live=False):
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
            post = self.sub.submit(title, content, send_replies=False)
            if settings["replaceSticky"] and not settings["testingMode"]:
                try:
                    checkPost = self.sub.sticky(number=2)
                    self.sub.sticky(number=1).mod.sticky(state=False)
                except Exception as e:
                    print("Error while removing top sticky in postToSubreddit: {}".format(e))
            if not settings["newFormat"]:
                post.mod.sticky()
            return post
        except Exception as e:
            print("Error in postToSubreddit: {}".format(e))