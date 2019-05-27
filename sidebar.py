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
import auxiliary as aux
import templates as tp


#Reload modules
reload(aux)

currentYear = 2019
prevYear = 2018

class Sidebar():

    def __init__(self, sub, r, settings):
        self.r = r
        self.sub = sub
        self.settings = settings
    
    def insertText(self, text, beginMarker=-1, endMarker=-1):
        """
        Inserts the given text in between the two markers in the text. If one marker is not given, then it places it right before/after the existing marker
        """
        try:
            #Load old sidebar text
            oldSidebar = self.sub.mod.settings()["description"]
            
            #Check if any markers are given
            if beginMarker == -1 and endMarker == -1:
                return False
                
            #If so, check if the begin marker is missing
            elif beginMarker == -1:
                #In which case, check if the end marker is present
                endIndex = oldSidebar.find(endMarker)
                if endIndex == -1:
                    return False
                    
                #And inject the given text before the end marker
                newSidebar = oldSidebar[:endIndex] + text + oldSidebar[endIndex:]
            
            #Else check if the end marker is missing
            elif endMarker == -1:
                #In which case, check if the begin marker is present
                beginIndex = oldSidebar.find(beginMarker)+len(beginMarker)
                if beginIndex == -1:
                    return False
                
                #And inject the given text after the begin marker
                newSidebar = oldSidebar[:beginIndex] + text + oldSidebar[beginIndex:]
            
            #If no markers are missing...
            else:
                #Check if the given markers are present
                beginIndex = oldSidebar.find(beginMarker)+len(beginMarker)
                endIndex = oldSidebar.find(endMarker)
                if beginIndex == -1 or endIndex == -1:
                    return False
                
                #And inject the given text in between the two markers
                newSidebar = oldSidebar[:beginIndex] + text + oldSidebar[endIndex:]
            
            #Upload the new sidebar text to the subreddit
            self.sub.mod.update(description=newSidebar)
            return True
        except Exception as e:
            print("Error in insertText: {}".format(e))
            return False
        
    def updateCountdown(self, currentTime):
        """
        Updates the countdown in the sidebar of the subreddit
        """
        print("Updating the countdown in the F1 sidebar")
        
        #Figure out the relevant races
        nextRace = aux.nextDate().raceTime
        prevRace = aux.prevDate().raceTime
        
        #Define markers in sidebar
        beginMarker = "[](/countDownBegin)"
        endMarker = "[](/countDownEnd)"
        try:
            #Check if race is still ongoing
            if currentTime < (prevRace + datetime.timedelta(hours=2, minutes=30)) and prevRace < currentTime:
                countdown = "In progress"
                
                #Use insertText to update the countdown
                success = self.insertText(countdown, beginMarker, endMarker)
            else:
                #Figure out the text in the countdown
                delta = nextRace - currentTime
                hours = int((delta.seconds - delta.seconds%3600)/3600)
                minutes = int((delta.seconds%3600)/60)
                countdown = "{0} day{1}, {2} hour{3} and {4} minute{5}".format(delta.days, "s"*(delta.days != 1), hours, "s"*(hours != 1),  minutes, "s"*(minutes != 1))
                
                #Use insertText to update the countdown
                success = self.insertText(countdown, beginMarker, endMarker)
            
            #Inform human of result
            if success:
                print("Successfully updated the countdown")
            else:
                print("Encountered a problem while updating the countdown")
        except Exception as e:
            print "Error in updateCountdown: {}".format(e)
            
    def updateSidebarInfo(self):
        """
        Updates all the race-related information in the sidebar
        """
        
        print("Updating the info in the F1 sidebar")
        
        try:
            #Define all the markers
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
            beginMarkerDriverSide = "[](/beginDriverSide)"
            endMarkerDriverSide = "[](/endDriverSide)"
            beginMarkerTeamSide = "[](/beginTeamSide)"
            endMarkerTeamSide = "[](/endTeamSide)"
            
            #Find the next race
            w = aux.nextDate()
            
            #Format the section on the name of the next race
            infoHead = "{0} Grand Prix\n - {1}, {2}".format(w.namean, w.city, w.country)
            
            #Format the section on the event schedule
            infoSched = "\n>|Session | Time (UTC)\n|-|-\nFree Practice 1|{0} • {1:02d}:{2:02d}\nFree Practice 2|{3} • {4:02d}:{5:02d}\nFree Practice 3|{6} • {7:02d}:{8:02d}\nQualifying|{9} • {10:02d}:{11:02d}\nRace|{12} • {13:02d}:{14:02d}".format(aux.weekdayToWord(w.fp1Time.weekday()), w.fp1Time.hour, w.fp1Time.minute, aux.weekdayToWord(w.fp2Time.weekday()), w.fp2Time.hour, w.fp2Time.minute, aux.weekdayToWord(w.fp3Time.weekday()), w.fp3Time.hour, w.fp3Time.minute, aux.weekdayToWord(w.qualiTime.weekday()), w.qualiTime.hour, w.qualiTime.minute, aux.weekdayToWord(w.raceTime.weekday()), w.raceTime.hour, w.raceTime.minute)
            
            #Format the section on the circuit
            infoCirc = "{0}\n>\n|||\n|-|-\nLaps|{1}\n|Circuit Length|{2} km ({3:.3f} mi)\nRace Length|{4} ({5:.3f} mi)\nFirst Held|{6}\nLap Record|{7} ([]({8}) {9}, {10}, {11})\nLinks|[Track Guide]({12}) - [Wikipedia]({13})".format(w.circuit, w.laps, w.length, w.length*0.62137, w.distance, w.distance*0.62137, w.firstHeld, w.lapRecordTime, w.lapRecordFlag, aux.abbrevName(w.lapRecordHolder), w.lapRecordTeam, w.lapRecordYear, w.linkF1, w.linkWikiRace)
            
            #Format the section on the previous year
            infoLast = "\n[]({0}) {1}, {2}, {3}\n> #Podium\n[]({4}) {5}, {6}\n> \n[]({7}) {8}, {9}, {10}\n> \n[]({11}) {12}, {13}, {14}\n> \n#Fastest Lap\n[]({15}) {16}, {17}, {18}".format(w.prevYearPoleFlag, w.prevYearPoleHolder, w.prevYearPoleTeam, w.prevYearPoleTime, w.prevYearWinnerFlag, aux.abbrevName(w.prevYearWinner), w.prevYearWinnerTeam, w.prevYearSecondFlag, aux.abbrevName(w.prevYearSecond), w.prevYearSecondTeam, w.prevYearSecondDelta, w.prevYearThirdFlag, aux.abbrevName(w.prevYearThird), w.prevYearThirdTeam, w.prevYearThirdDelta, w.prevYearFastestFlag, w.prevYearFastestHolder, w.prevYearFastestTeam, w.prevYearFastestTime)
            
            #Update all the information
            self.insertText(infoHead, beginMarkerHead, endMarkerHead)
            self.insertText(infoSched, beginMarkerSched, endMarkerSched)
            self.insertText(infoCirc, beginMarkerCirc, endMarkerCirc)
            self.insertText(infoLast, beginMarkerLast, endMarkerLast)
            
            #Try to upload the first sidebar image
            try:
                self.sub.stylesheet.upload("race-pic", "img/{}-1.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 1: {}".format(e))
                
            #Try to upload the second sidebar image
            try:
                self.sub.stylesheet.upload("race-pic-2", "img/{}-2.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 2: {}".format(e))
            
            #Try to upload the third sidebar image
            try:
                self.sub.stylesheet.upload("race-pic-3", "img/{}-3.png".format(w.country.lower().replace(" ", "")))
            except Exception as e:
                print("Failed to upload race pic 3: {}".format(e))
            
            #Try to upload the circuit map
            try:
                self.sub.stylesheet.upload("circuit-map", "img/{}-circuit.png".format(w.country.lower().replace(" ", "")))
                
                #If that works, also update the text
                self.insertText(w.circuit, beginMarkerTrack, endMarkerTrack)
            except Exception as e:
                print("Failed to upload circuit map: {}".format(e))
            
            #Reupload stylesheet to make sure the images work
            try:
                self.sub.stylesheet.update(self.sub.stylesheet().stylesheet, reason="Updating race pics and circuit map")
            except Exception as e:
                print("Failed to update stylesheet: {}".format(e))
                
            #Attempt to update championship standings
            try:
                #Retrieve the dropdown menu standings
                driverStand = ws.driverStandings(type=0)
                teamStand = ws.teamStandings(type=0)
                
                #Retrieve the main sidebar standings (or the other way around, I'm not sure)
                driverStandSide = ws.driverStandings(type=1)
                teamStandSide = ws.teamStandings(type=1)
                
                #If successfully retrieved...
                if driverStand and teamStand:
                    self.insertText(driverStand, beginMarkerDriver, endMarkerDriver)
                    self.insertText(teamStand, beginMarkerTeam, endMarkerTeam)
                if driverStandSide and teamStandSide:
                    self.insertText(driverStandSide, beginMarkerDriverSide, endMarkerDriverSide)
                    self.insertText(teamStandSide, beginMarkerTeamSide, endMarkerTeamSide)
            except Exception as e:
                print("Failed to update driver and team standings: {}".format(e))
            
            print("Successfully updated the info in the sidebar")
            return "{} Grand Prix".format(w.namean)
        except Exception as e:
            print("Error in updateSidebarInfo: {}".format(e))
            return False
    
    def updateWeatherPrediction(self, owm, forecast):
        """
        Updates the weather prediction in the sidebar of the subreddit
        """
        print("Updating the weather prediction")
        
        #Get current time
        currentTime = datetime.datetime.utcnow()
        
        #Define markers
        beginMarker = "[](/weatherBegin)"
        endMarker = "[](/weatherEnd)"
        
        #Find next weekend
        nextWeekend = aux.nextDate()
        
        #Obtain session times of next weekend
        fp1Time = nextWeekend.fp1Time
        fp2Time = nextWeekend.fp2Time
        fp3Time = nextWeekend.fp3Time
        qualiTime = nextWeekend.qualiTime
        raceTime = nextWeekend.raceTime
        
        try:
            #Get forecast object
            fc = aux.getForecast(owm)
            
            #If not successful, keep old one
            if fc == False:
                fc = forecast
            
            #If sufficiently close to the race
            if raceTime - datetime.timedelta(days=4, hours=12, minutes=10) < currentTime:
                #Try to obtain the forecasts for each of the sessions
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
                
                #Format the prediction
                prediction = "Weather Prediction"
                for i in range(len(statusList)):
                    if statusList[i] != 0:
                        prediction += "\n> - {0}\n>  - []({1})\n>  - {2}\n>  - {3} °C / {4} °F".format(abbrev[i], aux.weatherIcon(statusList[i].get_weather_icon_name()), aux.weatherChange(aux.firstCaps(statusList[i].get_detailed_status())), int(statusList[i].get_temperature(unit="celsius")["temp"]), int(statusList[i].get_temperature(unit="fahrenheit")["temp"]))
                prediction += "\n>\n> [Link to source](http://openweathermap.org/city/{})".format(nextWeekend.weatherID)
                
                #Upload the prediction to sidebar
                self.insertText(prediction, beginMarker, endMarker)
            else:
                #Upload the placeholder to sidebar
                self.insertText("Weather Prediction\n> The weather prediction is not yet available.", beginMarker, endMarker)
            print("Sucessfully updated the sidebar")
            return fc
        except Exception as e:
            print("Error in updateWeatherPrediction: {}".format(e))
            return False
            
    def updateTopBar(self, post, weekend, abbrev):
        """
        Updates the top bar of the subreddit
        """
        
        #Define markers
        beginMarker = "[](/topBegin)"
        endMarker = "[](/topEnd)"
        
        try:
            #Don't change anything in testing mode
            if self.settings["testingMode"] == True:
                return False
                
            #If Hub, then clear the top bar before adding Hub
            elif abbrev == "Hub":
                insertString = "[]({0})\n- [{1}]({2})".format(weekend.flag, abbrev, post.shortlink)
                self.insertText(insertString, beginMarker, endMarker)
            
            #Else just add to it
            else:
                insertString = " [{0}]({1})".format(abbrev, post.shortlink)
                self.insertText(insertString, -1, endMarker)
        except Exception as e:
            print("Error in updateTopBar: {}".format(e))
    
    def updateHeaderQuote(self):
        """
        Updates the quote in the header of the /r/formula1 subreddit
        """
        #Define markers
        beginMarker = "[](/beginHeaderQuote)"
        endMarker = "[](/endHeaderQuote)"
        
        #Define relevant lists
        drivers_list = ["Hamilton", "Vettel", "Bottas", "Räikkönen", "Verstappen", "Ricciardo", "Pérez", "Magnussen", "Hülkenberg", "Sainz", "Grosjean", "Gasly", "Leclerc", "Stroll", "Russell", "Albon", "Giovinazzi", "Kubica", "Kvyat", "Norris"]
        old_drivers_list = ["Jim Clark", "Juan Manuel Fangio", "Jackie Stewart", "Alberto Ascari", "Guiseppe Farina", "Stirling Moss", "John Surtees", "Emerson Fittipaldi", "Nelson Piquet", "Ayrton Senna", "Alain Prost", "Niki Lauda", "Graham Hill", "Mika Häkkinen",  "Michael Schumacher", "Nigel Mansell", "Jochen Rindt", "Jack Brabham", "Ronnie Peterson", "Gilles Villeneuve", "Bruce Mclaren", "Mario Andretti", "Fernando Alonso"]
        shitty_old_drivers_list = ["Tarso Marques", "Chanoch Nissany", "Yuji Ide", "Taki Inoue", "Andrea de Cesaris", "Marco Apicella", "Alex Yoong", "Rikky Von Opel", "Satoru Nakajima", "Andrea Montermini", "Ricardo Rosset", "Philippe Alliot", "Philippe Streiff", "Manfred Winkelhock", "Johathan Palmer", "Eliseo Salazar", "Ivan Capelli", "Johnny Dumfries", "Stefano Modena", "Gabriele Tarquini", "Pierre-Henry Raphanel", "Maurício Gugelmin", "Bruno Giacomelli", "Olivier Beretta", "Jos Verstappen", "Andrea Montermini", "Aguri Suzuki", "Gastón Mazzacane"]
        teams_list = ["Mercedes", "Ferrari", "Red Bull", "Renault", "Haas", "McLaren", "Force India", "Toro Rosso", "Sauber", "Williams"]
        mods_list = ["Mulsanne", "HeikkiKovalainen", "empw", "whatthefat", "Redbiertje", "jeppe96", "BottasWMR", "flipjj"]
        
        try:
            #Retrieve templates from subreddit wiki
            wikiContent = self.sub.wiki['headertemplates'].content_md
            templates = [line[1:].lstrip() for line in wikiContent.split("---")[1].lstrip().rstrip().split("\r\n")]
            
            #Select random template
            selectedTemplate = random.choice(templates)+" "
            
            #Get substitutes
            rand_driver = random.choice(drivers_list)
            rand_old = random.choice(old_drivers_list)
            rand_shitty = random.choice(shitty_old_drivers_list)
            rand_team = random.choice(teams_list)
            rand_mod = random.choice(mods_list)
            rand_country = random.choice(weekends.allWeekends).country
            rand_city = random.choice(weekends.allWeekends).city
            next_country = aux.nextDate().country
            next_city = aux.nextDate().city
            prev_country = aux.prevDate().country
            prev_city = aux.prevDate().city
            
            #Get template and substitute placeholders
            headerQuote = selectedTemplate.replace("<mod>", rand_mod).replace("<driver>", rand_driver).replace("<olddriver>", rand_old).replace("<shittydriver>", rand_shitty).replace("<team>", rand_team).replace("<country>", rand_country).replace("<city>", rand_city).replace("<nextcountry>", next_country).replace("<nextcity>", next_city).replace("<prevcountry>", prev_country).replace("<prevcity>", prev_city)
            
            #Report the selected quote
            print("Updating header quote: {}".format(headerQuote))
            
            #Upload new quote to sidebar
            self.insertText(headerQuote, beginMarker, endMarker)
            return True
        except Exception as e:
            print("Error in updateHeaderQuote: {}".format(e))
            return False
