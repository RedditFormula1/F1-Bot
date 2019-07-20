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
import random
import numpy as np
import weekends
import webscraper as ws
import templates as tp
import auxiliary as aux
import sidebar
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import TfidfVectorizer


#Reload modules
reload(sidebar)
reload(aux)

currentYear = 2019
prevYear = 2018

class Subreddit():

    def __init__(self, r, sub, settings):
        self.r = r
        self.sub = sub
        self.settings = settings
        self.sidebar = sidebar.Sidebar(self.sub, self.r, self.settings)

    def updateFlairCounts(self, redditor):
        """
        Updates the list of flair counts in the wiki
        """

        try:
            #Get current time
            currentTime = datetime.datetime.utcnow()

            #Prepare flairs dictionary
            flairs = {}

            #Iterate over all flairs on the subreddit
            for flair in self.sub.flair(limit=None):

                #Add flair to dictionary
                flairName = flair['flair_css_class']
                if flairName not in flairs:
                    flairs[flairName] = 0
                flairs[flairName] += 1

            #Sort results by counts
            sorted_flairs = sorted(flairs.items(), key=lambda x: x[1], reverse=True)

            #Update wiki page
            wikiPage = self.sub.wiki['flaircounts']
            content = "# Formula 1 flair counts\n\n**[Click here to update the flair counts](https://www.reddit.com/message/compose?to=F1-Bot&subject=command&message=flairs)**\n\nLast update: {0} {1} {2}, {3:02d}:{4:02d}\n\n---\n\n## Flair counts\n\n|CSS class|Count|\n|--:|:--|".format(currentTime.day, aux.monthToWord(currentTime.month), currentTime.year, currentTime.hour, currentTime.minute)
            for CSS, count in sorted_flairs:
                content += "\n|{0}|{1}|".format(CSS, count)
            wikiPage.edit(content, reason="{} requested an update.".format(redditor))
        except Exception as e:
            print("Error in updateFlairCounts: {}".format(e))

    def postToSubreddit(self, w, thread, owm=False, fc=False, live=False):
        """
        Posts a discussion post to the subreddit
        """

        #Determine which kind of thread it should be (obsolete)
        if live:
            type = "Live Thread"
        else:
            type = "Discussion"
        try:
            #Get session times for the table
            qualiUTC = "{0} {1:02d}:{2:02d}".format(aux.weekdayToWord(w.qualiTime.weekday()), w.qualiTime.hour, w.qualiTime.minute)
            raceUTC = "{0} {1:02d}:{2:02d}".format(aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.hour, w.raceTime.minute)
            fp1UTC = "{0} {1:02d}:{2:02d}".format(aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.hour, w.fp1Time.minute)
            fp2UTC = "{0} {1:02d}:{2:02d}".format(aux.weekdayToWord(w.fp2Time.weekday()), w.fp2Time.hour, w.fp2Time.minute)
            fp3UTC = "{0} {1:02d}:{2:02d}".format(aux.weekdayToWord(w.fp3Time.weekday()), w.fp3Time.hour, w.fp3Time.minute)

            #Weekend Hub post
            if thread == "Weekend Hub":
                try:
                    #Get weather report for the coming sessions based on existing weather forecast
                    fp1Status = fc.get_weather_at(w.fp1Time)
                    fp2Status = fc.get_weather_at(w.fp2Time)
                    fp3Status = fc.get_weather_at(w.fp3Time)
                    qualiStatus = fc.get_weather_at(w.qualiTime)
                    raceStatus = fc.get_weather_at(w.raceTime)
                except Exception as e:
                    #Else try to obtain a new weather forecast
                    print("Retrying to get a weather forecast")
                    fc = aux.getForecast(owm)
                    fp1Status = fc.get_weather_at(w.fp1Time)
                    fp2Status = fc.get_weather_at(w.fp2Time)
                    fp3Status = fc.get_weather_at(w.fp3Time)
                    qualiStatus = fc.get_weather_at(w.qualiTime)
                    raceStatus = fc.get_weather_at(w.raceTime)
                #Format the title of the weekend hub
                title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)

                #Format the content of the weekend hub
                content = tp.hub_template.format(w.round, w.country, w.flag, fp1UTC, aux.weatherIcon(fp1Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp1Status.get_detailed_status())), int(fp1Status.get_temperature(unit="celsius")["temp"]), int(fp1Status.get_temperature(unit="fahrenheit")["temp"]), fp2UTC, aux.weatherIcon(fp2Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp2Status.get_detailed_status())), int(fp2Status.get_temperature(unit="celsius")["temp"]), int(fp2Status.get_temperature(unit="fahrenheit")["temp"]), fp3UTC, aux.weatherIcon(fp3Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp3Status.get_detailed_status())), int(fp3Status.get_temperature(unit="celsius")["temp"]), int(fp3Status.get_temperature(unit="fahrenheit")["temp"]), qualiUTC, aux.weatherIcon(qualiStatus.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(qualiStatus.get_detailed_status())), int(qualiStatus.get_temperature(unit="celsius")["temp"]), int(qualiStatus.get_temperature(unit="fahrenheit")["temp"]), raceUTC, aux.weatherIcon(raceStatus.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(raceStatus.get_detailed_status())), int(raceStatus.get_temperature(unit="celsius")["temp"]), int(raceStatus.get_temperature(unit="fahrenheit")["temp"]))

            #Day after Debrief thread
            elif thread == "Day after Debrief":
                #Format the title of the DaD thread
                title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)

                #Format the content of the DaD thread
                content = tp.dad_template.format(w.round, w.country, w.flag, w.city)

            #Daily Discussion thread
            elif thread == 'Daily Discussion':
                #Get the current date
                currentTime = datetime.datetime.utcnow()
                date = str(currentTime.day) + ' ' + aux.monthToWord(currentTime.month) + ' ' + str(currentTime.year)

                #Format the title of DD thread

                title = 'Daily Discussion - ' + date

                #Format the content of DD thread
                content = 'This thread is for general discussion of current topics in F1 and quick questions about the sport.'

            #One of the post-session threads
            elif thread == "Post Qualifying" or thread == "Post Race":
                #Format the title of the thread
                title = "{0} {1} Grand Prix - {2} Discussion".format(currentYear, w.namean, thread)

                #Format the content of the thread
                #                                         0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23           24              25                   26                  27                  28             29              30                       31                       32                    33              34              35                  36                  37               38          39            40             41            42      43       44
                content = tp.post_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC)

            #Else it is a regular session thread
            else:
                #If it is a pre-race thread, then obtain starting grid
                if thread == "Pre Race" or (thread == "Race" and self.settings["newFormat"]):
                    webscraperOutput = ws.startingGrid(w)
                    if webscraperOutput == False:
                        grid = ""
                    else:
                        grid = "---\n\n{}\n\n".format(webscraperOutput)
                #Else just insert nothing
                else:
                    grid = ""

                #Format the title of the thread
                title = "{0} {1} Grand Prix - {2} {3}".format(currentYear, w.namean, thread, type)

                #Format the content of the thread
                if self.settings["newFormat"]:
                    if live:
                        #                                          0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23            24              25                   26                  27                  28             29              30                       31                       32                    33                  34              35                  36                  37               38          39            40             41            42      43      44    45
                        content = tp.new_session_template_live.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
                    else:
                        #                                          0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23            24              25                   26                  27                  28             29              30                       31                       32                    33                  34              35                  36                  37               38          39            40             41            42      43      44    45
                        content = tp.new_session_template_disc.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)
                else:
                    #                                          0          1        2         3                        4                        5                    6                                 7                           8                        9                 10       11      12         13        14            15           16        17              18                  19               20                 21               22              23            24              25                   26                  27                  28             29              30                       31                       32                    33                  34              35                  36                  37               38          39            40             41            42      43      44    45
                    content = tp.old_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit, fp1UTC, fp2UTC, fp3UTC, grid)

            #Submit the post
            post = self.sub.submit(title, content, send_replies=False)

            #If stickies should be replaced, then cycle them through
            if self.settings["replaceSticky"] and not self.settings["testingMode"]:
                try:
                    checkPost = self.sub.sticky(number=2)
                    self.sub.sticky(number=1).mod.sticky(state=False)
                except Exception as e:
                    print("Error while removing top sticky in postToSubreddit: {}".format(e))
            if not self.settings["newFormat"]:
                post.mod.sticky()
            return post
        except Exception as e:
            print("Error in postToSubreddit: {}".format(e))

    def checkAll(self):
        """
        Checks /r/all to see if there are any posts from /r/formula1. Any posts from /r/formula1 in /r/all will receive a flair
        """
        #Get /r/all subreddit
        all = self.r.subreddit("all")

        #Iterate over the front page
        for submission in all.hot(limit=50):
            #If post comes from our subreddit and does not already have the /r/all flair
            if submission.subreddit.display_name == self.sub.display_name and submission.link_flair_css_class != "sub-all":
                #Proudly report this good news to the boss
                print("Found a new post in /r/all!")

                #Give it the flair
                try:
                    if submission.link_flair_text != None:
                        submission.mod.flair(text="{} /r/all".format(submission.link_flair_text), css_class="sub-all")
                    else:
                        submission.mod.flair(text="/r/all", css_class="sub-all")
                except Exception as e:
                    print("Error in checkAll: {}".format(e))

    def tweetTopPost(self, twitter):
        """
        Posts the top tweet from the subreddit to Twitter.
        """
        print("Tweeting top post of the day")

        try:
            #Retrieve top post from the last day
            topPosts = self.sub.top("day", limit=1)

            #Do silly trick because the output is a listing generator
            for topPost in topPosts:
                break

            #Check if it has a decent score
            if topPost.score >= self.settings["scoreThreshold"]:
                #Retrieve tweet templates from the subreddit
                wikiContent = self.sub.wiki['tweettemplates'].content_md
                templates = [line[1:].lstrip() for line in wikiContent.split("---")[1].lstrip().rstrip().split("\r\n")]

                #Select random template
                selectedTemplate = random.choice(templates)

                #Abbreviate post title if necessary
                if len(topPost.title) > 300:
                    topPost_title = topPost.title[:300]+'...'
                else:
                    topPost_title = topPost.title

                #Fill in placeholders
                tweetText = selectedTemplate.replace("<link>", topPost.shortlink).replace("<title>", topPost_title).replace("<score>", str(topPost.score)).replace("<user>", "/u/"+topPost.author.name)

                #Try to submit the tweet (if testing mode is off)
                try:
                    if not self.settings["testingMode"]:
                        tweet = twitter.update_status(tweetText)
                        print("Successfully posted a tweet")
                except Exception as e:
                    print("Error in tweetTopPost (Twitter section): {}".format(e))
        except Exception as e:
            print("Error in checkTopPost: {}".format(e))

    def getTrafficReport(self):
        """
        Generates and formats a traffic report from the subreddit
        """

        try:
            #Get current time
            currentTime = datetime.datetime.utcnow()

            #Retrieve traffic dictionary and split out the lists
            traffic_dict = self.sub.traffic()
            day_stats = traffic_dict['day']
            hour_stats = traffic_dict['hour']
            month_stats = traffic_dict['month']

            #Prepare report
            report = "#Traffic stats for /r/formula1\n\nGenerated on {0} {1} {2}, {3:02d}:{4:02d}\n\nAll times in UTC\n\n##Traffic by day\n\n|Date|Unique users|Total page views|Subscribes|\n|:--|:--|:--|:--|".format(currentTime.day, aux.monthToWord(currentTime.month), currentTime.year, currentTime.hour, currentTime.minute)

            #For each day, add a line to the report
            for timestamp, uniques, pageviews, subs in day_stats:
                date = datetime.datetime.fromtimestamp(timestamp)
                dateString = "{0} {1} {2}".format(date.year, aux.monthToWord(date.month), date.day)
                if pageviews != 0:
                    report += "\n|{0}|{1}|{2}|{3}|".format(dateString, uniques, pageviews, subs)

            #Add intermediate part to the report
            report += "\n\n##Traffic by hour\n\n|Date|Unique users|Total page views|\n|:--|:--|:--|"

            #For each hour, add a line to the report
            for timestamp, uniques, pageviews in hour_stats:
                date = datetime.datetime.fromtimestamp(timestamp)
                dateString = "{0} {1}, {2:02d}:00".format(aux.monthToWord(date.month), date.day, date.hour)
                if pageviews != 0:
                    report += "\n|{0}|{1}|{2}|".format(dateString, uniques, pageviews)

            #Add intermediate part to the report
            report += "\n\n##Traffic by month\n\n|Date|Unique users|Total page views|\n|:--|:--|:--|"

            #For each month, add a line to the report
            for timestamp, uniques, pageviews in month_stats:
                date = datetime.datetime.fromtimestamp(timestamp)
                dateString = "{0} {1}".format(date.year, aux.monthToWord(date.month))
                if pageviews != 0:
                    report += "\n|{0}|{1}|{2}|".format(dateString, uniques, pageviews)

            #Return report
            return report
        except Exception as e:
            print("Error in getTrafficReport: {}".format(e))
            return False

    def storePostTitles(self):
        """
        Stores the titles of new posts in a file for repost-checking purposes
        """
        try:
            #Load previous post data
            data = np.loadtxt("data/postTitles.tsv", delimiter="\t", comments="#", dtype="str")
            IDs, titles = data.T

            #Open data file
            data_file = open("data/postTitles.tsv", "a")

            #Go through all new posts, and add them if necessary
            for submission in self.sub.new(limit=100):
                if submission.id not in IDs:
                    if submission.domain != "self.formula1":
                        data_file.write("\n{0}\t{1}".format(submission.id, submission.title))
                else:
                    break

            #Close the file again
            data_file.close()
        except Exception as e:
            print("Error in storePostTitles: {}".format(e))

    def checkReposts(self):
        """
        Checks for reposts in the subreddit
        """
        try:
            #Set amount of posts to look back in
            OCdistance = 200

            #Load previous post data
            data = np.loadtxt("data/postTitles.tsv", delimiter="\t", comments="#", dtype="str")
            IDs, titles = data.T

            #Create tf.idf matrix of old titles
            tf = TfidfVectorizer(stop_words='english', ngram_range=(1, 1))
            X = tf.fit_transform(titles)

            #Browse new posts
            for submission in self.sub.new(limit=100):
                if submission.id not in IDs:
                    #Check against filter
                    if submission.domain != "self.formula1" and submission.author != "xScottieHD" and submission.author != "RoundHeadedTwonk21":
                        #Throw title into repost checker
                        testingString = submission.title
                        search_query =  tf.transform([testingString])
                        cosine_similarities = linear_kernel(X, search_query).flatten()[-OCdistance:]
                        most_related_docs = cosine_similarities.argsort()[-10:][::-1]
                        if cosine_similarities[most_related_docs[0]] > 0.8:
                            OrigPost = r.submission(id=IDs[-OCdistance:][most_related_docs[0]])
                            if not OrigPost.removed and not OrigPost.selftext == "[deleted]":
                                #Report the post to the moderators
                                submission.report("Possible repost ({0}%): https://redd.it/{1}".format(int(100*cosine_similarities[most_related_docs[0]]), OrigPost.id))
                                #redbiertje.message("Possible repost", "Hi there,\n\nI've found the following post:\n\n[{0}]({1})\n\nwhich looks a lot like\n\n[{2}](https://redd.it/{3})\n\nPlease check if it's a repost.\n\n(Similarity: {4:4f})".format(submission.title, submission.permalink, OrigPost.title, OrigPost.id, cosine_similarities[most_related_docs[0]]))
                else:
                    break
        except Exception as e:
            print("Error in checkReposts: {}".format(e))
