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
import os


currentYear = 2020
prevYear = 2019
moderators = ["ddigger", "Mulsanne", "HeikkiKovalainen", "halfslapper", "empw", "whatthefat", "Redbiertje", "jeppe96", "flipjj", "Effulgency", "Blanchimont", "elusive_username", "AshKals", "UnmeshDatta26", "AnilP228", "anneomoly", "balls2brakeLate44", "overspeeed"]

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
            
    def postToSubreddit(self, w, thread, owm=False, fc=False, live=False, sticky=True):
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
            
            if w.lastYear:
                lastyear = tp.lastyear_template.format(w.lapRecordFlag, w.lapRecordHolder, w.lapRecordTeam, w.lapRecordYear, w.lapRecordTime, w.lastYear, w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.lastYear, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime, w.lastYear, w.prevYearWinnerFlag, w.prevYearWinner, w.prevYearWinnerTeam)
            else:
                lastyear = ""
            
            #Fan Hub post
            if thread == "Fan Hub":
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
                #Format the title of the fan hub
                title = "/r/formula1 goes to the {0} {1} Grand Prix - On-track Fan Hub".format(currentYear, w.namean)
                
                #Format the content of the fan hub
                content = tp.hub_template.format(w.round, w.country, w.flag, fp1UTC, aux.weatherIcon(fp1Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp1Status.get_detailed_status())), int(fp1Status.get_temperature(unit="celsius")["temp"]), int(fp1Status.get_temperature(unit="fahrenheit")["temp"]), fp2UTC, aux.weatherIcon(fp2Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp2Status.get_detailed_status())), int(fp2Status.get_temperature(unit="celsius")["temp"]), int(fp2Status.get_temperature(unit="fahrenheit")["temp"]), fp3UTC, aux.weatherIcon(fp3Status.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(fp3Status.get_detailed_status())), int(fp3Status.get_temperature(unit="celsius")["temp"]), int(fp3Status.get_temperature(unit="fahrenheit")["temp"]), qualiUTC, aux.weatherIcon(qualiStatus.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(qualiStatus.get_detailed_status())), int(qualiStatus.get_temperature(unit="celsius")["temp"]), int(qualiStatus.get_temperature(unit="fahrenheit")["temp"]), raceUTC, aux.weatherIcon(raceStatus.get_weather_icon_name()), aux.weatherChange(aux.firstCaps(raceStatus.get_detailed_status())), int(raceStatus.get_temperature(unit="celsius")["temp"]), int(raceStatus.get_temperature(unit="fahrenheit")["temp"]), currentYear, w.namean)
            
            #Day after Debrief thread
            elif thread == "Day after Debrief":
                #Format the title of the DaD thread
                title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)
                
                #Format the content of the DaD thread
                content = tp.dad_template.format(w.round, w.country, w.flag, w.city)
            
            #Daily Discussion thread
            elif thread == "Daily Discussion":
                #Get the current date
                currentTime = datetime.datetime.utcnow()
                date = "{} {} {}".format(currentTime.day, aux.monthToWord(currentTime.month), currentTime.year)

                #Format the title of DD thread
                title = '/r/Formula1 Daily Discussion - ' + date
                
                #Retrieve random facts from subreddit wiki
                wikiContent = self.sub.wiki['f1bot-ddfacts'].content_md
                templates = [line[1:].lstrip() for line in wikiContent.split("---")[1].lstrip().rstrip().split("\r\n")]
                facts = random.sample(templates, 3)
                
                #Retrieve top 5 posts of the sub
                topPosts = self.sub.top("day", limit=5)
                topTitles = []
                topLinks = []
                for post in topPosts:
                    topTitles.append(post.title)
                    topLinks.append(post.shortlink)

                #Format the content of DD thread
                content = tp.dd_template.format(facts[0], facts[1], facts[2], topTitles[0], topLinks[0], topTitles[1], topLinks[1], topTitles[2], topLinks[2], topTitles[3], topLinks[3], topTitles[4], topLinks[4])
                #content = 'This thread is for general discussion of current topics in F1 and quick questions about the sport.'
                
            #Media Hub thread
            elif thread == "Media Hub":
                #Format the title of the Media Hub thread
                title = "{0} {1} Grand Prix - {2}".format(currentYear, w.namean, thread)

                #Format the content of the Media Hub thread
                content = tp.mh_template.format(w.round, w.country, w.flag, self.getHighlights(w.raceTime), 'Driver | Network \n :--|:--')
                
            #One of the post-session threads
            elif thread == "Post Qualifying" or thread == "Post Race":
                #Format the title of the thread
                title = "{0} {1} Grand Prix - {2} Discussion".format(currentYear, w.namean, thread)
                
                #Format the content of the thread
                #                                         0        1          2       3            4                                       5              6                                 7                                        8               9                                  10      11      12      13      14        15       16         17        18                19      20          21                  22        23        24              25         26
                content = tp.post_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, fp1UTC, fp2UTC, fp3UTC, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, lastyear, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit)
            
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
                        #                                        0        1          2       3            4                                       5              6                                 7                                        8               9                                  10      11      12      13      14        15       16         17        18                19      20          21                  22        23    24        25              26         27
                        content = tp.new_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, fp1UTC, fp2UTC, fp3UTC, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, lastyear, grid, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit)
                    else:
                        #                                        0        1          2       3            4                                       5              6                                 7                                        8               9                                  10      11      12      13      14        15       16         17        18                19      20          21                  22        23    24        25              26         27
                        content = tp.new_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, fp1UTC, fp2UTC, fp3UTC, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, lastyear, grid, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit)
                else:
                    #                                        0        1          2       3            4                                       5              6                                 7                                        8               9                                  10      11      12      13      14        15       16         17        18                19      20          21                  22        23    24        25              26         27
                    content = tp.old_session_template.format(w.round, w.country, w.flag, w.fullTitle, aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.day, aux.monthToWord(w.fp1Time.month), aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.day, aux.monthToWord(w.raceTime.month), w.city, fp1UTC, fp2UTC, fp3UTC, qualiUTC, raceUTC, w.circuit, w.length, w.length*0.62137, w.laps, w.distance, w.distance*0.62137, lastyear, grid, w.linkF1, w.linkWikiRace, w.circuit, w.linkWikiCircuit)
            
            #Submit the post
            post = self.sub.submit(title, content, send_replies=False)
            
            #If stickies should be replaced, then cycle them through
            if self.settings["replaceSticky"] and not self.settings["testingMode"]:
                try:
                    checkPost = self.sub.sticky(number=2)
                    self.sub.sticky(number=1).mod.sticky(state=False)
                except Exception as e:
                    print("Error while removing top sticky in postToSubreddit: {}".format(e))
            if not self.settings["newFormat"] and sticky:
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
        print("[ ] Tweeting top post of the day", end="\r")
        
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
                        print("[x] Tweeting top post of the day")
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
            OCdistance = 1000
            sim_thres = 0.6
            
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
                        for doc in most_related_docs:
                            if cosine_similarities[doc] > 0.6:
                                orig_post = self.r.submission(id=IDs[-OCdistance:][doc])
                                if not orig_post.removed and not orig_post.selftext == "[deleted]":
                                    #Report the post to the moderators
                                    submission.report("Possible repost ({0}%): https://redd.it/{1}".format(int(100*cosine_similarities[most_related_docs[0]]), orig_post.id))
                                    break
                else:
                    break
        except Exception as e:
            print("Error in checkReposts: {}".format(e))
            
    def getHighlights(self, raceTime):
        """
        Uses Pushshift search to find race highlights in past 3 hours
        Written by: BottasWMR
        """
        giffers = ['BottasWMR','Mark4211','exiledtie', 'buschjp', 'overspeeed', 'gamekarma86', 'magony', 'Farrisioso', 'peke_f1']
        highlights = []
        race_timestamp = datetime.datetime.timestamp(raceTime)
        bodyText = 'Highlight|Thread\n:--|:--\n'
        for giffer_name in giffers:
            try:
                giffer = self.r.redditor(giffer_name)
                for submission in giffer.submissions.new(limit=100):
                    if submission.created_utc > race_timestamp and submission.domain == "streamable.com" and submission.subreddit.display_name == "formula1":
                        highlights.append((submission.title, submission.url, submission.permalink, submission.created_utc))
            except Exception as e:
                print("Error in getHighlights: {}".format(e))
        highlights.sort(key=lambda tup: tup[3])
        for highlight in highlights:
            bodyText = bodyText + f'[{highlight[0]}]({highlight[1]}) | [Link]({highlight[2]}) \n'\

        return bodyText
        
    def logger(self, mode="comments"):
        """
        Log all new comments or posts
        """
        try:
            if mode == "comments":
                #Load previous post data
                IDs = []
                for line in aux.readlines_reverse("data/{}_comments.tsv".format(self.sub.display_name)):
                    values = line.split("\t")
                    IDs.append(values[0])
                    if len(IDs) >= 120:
                        break
                IDs = np.array(IDs)
                                
                #Open data file
                data_file = open("data/{}_comments.tsv".format(self.sub.display_name), "a")
                
                #Go through all new posts, and add them if necessary
                for comment in self.sub.comments(limit=25):
                    if comment.id not in IDs:
                        body = comment.body.replace("\n", " ").replace("\t", " ").strip()
                        if len(body) > 4000:
                            body = body[:4000]
                        data_file.write("\n{0}\t{1}\t{2}\t{3}".format(comment.id, comment.created_utc, comment.author.name, body))
                    else:
                        break
                    
                #Close the data file again
                data_file.close()
            
        except Exception as e:
            print("Error in subreddit.logger: {}".format(e))
            
    def modlogger(self):
        """
        Log modlog actions
        """
        try:
            print("[ ] Storing approved and removed comments", end="\r")
            
            IDs = []
            for line in aux.readlines_reverse("data/{}_modlogcomments.tsv".format(self.sub.display_name)):
                values = line.split("\t")
                IDs.append(values[0])
                if len(IDs) >= 120:
                    break
            for line in aux.readlines_reverse("data/{}_redditlegal.tsv".format(self.sub.display_name)):
                values = line.split("\t")
                IDs.append(values[0])
                if len(IDs) >= 240:
                    break
                
            IDs = np.array(IDs)
            
            #Open data file
            data_file = open("data/{}_modlogcomments.tsv".format(self.sub.display_name), "a")
            legal_file = open("data/{}_redditlegal.tsv".format(self.sub.display_name), "a")
            
            #Go through all new actions, and add them if necessary
            for action in self.sub.mod.log(limit=100):
                if action.id not in IDs:
                    if action.mod in moderators and (action.action == "removecomment" or action.action == "approvecomment"):
                        body = action.target_body.replace("\n", " ").replace("\t", " ").strip()
                        if len(body) > 4000:
                            body = body[:4000]
                        flag = 1 if action.action == "removecomment" else 0
                        data_file.write("\n{0}\t{1}\t{2}\t{3}\t{4}".format(action.id, action.created_utc, action.target_author, flag, body))
                    if action.mod == "Reddit Legal":
                        legal_file.write("\n{}\t{}\t{}\t{}".format(action.id, action.created_utc, action.target_author, action.target_permalink))
                        jeppe = self.r.redditor("jeppe96")
                        jeppe.message("Notification: Reddit Legal action", "Reddit Legal performed an action on /r/{} against the following post by /u/{}:\n\n{}\n\n".format(self.sub.display_name, action.target_author, action.target_permalink))
                        red = self.r.redditor("Redbiertje")
                        red.message("Notification: Reddit Legal action", "Reddit Legal performed an action on /r/{} against the following post by /u/{}:\n\n{}\n\n".format(self.sub.display_name, action.target_author, action.target_permalink))
                else:
                    break
            
            #Close the data file again
            data_file.close()
            legal_file.close()
            
            print("[x] Storing approved and removed comments")
            
        except Exception as e:
            print("Error in subreddit.modlogger: {}".format(e))
            
    def checkBanEvasion(self, username):
        """
        Checks activity against activity of ban list
        """
        try:
            checked_list = []
            user_activity = self.getUserActivity(username)
            user_activity.pop('formula1', None)
            for user in self.sub.banned():
                try:
                    activity = self.getUserActivity(user.name)
                    activity.pop('formula1', None)
                    checked_list.append((user.name, aux.similarity(user_activity, activity)))
                except Exception as e:
                    pass
            return sorted(checked_list, key=lambda x: x[1])[::-1]
            
        except Exception as e:
            print("Error in subreddit.checkBanEvasion: {}".format(e))
            return False
    
    def getUserActivity(self, username, comments=True, submissions=True):
        """
        Obtains list of subreddits in which the user has been active
        """
        try:
            #Prepare output dictionary
            output = {}
            
            #Get user object
            user = self.r.redditor(username)
            
            #If we want to count comment activity
            if comments:
                for comment in user.comments.new(limit=None):
                    subname = comment.subreddit.display_name
                    try:
                        output[subname] += 1
                    except KeyError:
                        output[subname] = 1
            
            #If we want to count submission activity
            if submissions:
                for submission in user.submissions.new(limit=None):
                    subname = submission.subreddit.display_name
                    try:
                        output[subname] += 1
                    except KeyError:
                        output[subname] = 1
                        
            return output
        
        except Exception as e:
            print("Error in subreddit.getUserActivity: {}".format(e))
            return False