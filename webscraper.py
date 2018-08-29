#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
18 Sep 2017
"""

#Imports
from __future__ import division
import urllib2
from math import ceil
from bs4 import BeautifulSoup
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from selenium import webdriver
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.options import Options
import datetime

currentYear = 2018

flagDriverDict = {"Lewis Hamilton": "gb",
    "Sebastian Vettel": "de",
    "Valtteri Bottas": "fi",
    "Daniel Ricciardo": "au",
    "Kimi Räikkönen": "fi",
    "Max Verstappen": "nl",
    "Sergio Perez": "mx",
    "Esteban Ocon": "fr",
    "Carlos Sainz": "es",
    "Nico Hulkenberg": "de",
    "Felipe Massa": "br",
    "Lance Stroll": "ca",
    "Romain Grosjean": "fr",
    "Kevin Magnussen": "dk",
    "Fernando Alonso": "es",
    "Jolyon Palmer": "gb",
    "Stoffel Vandoorne": "be",
    "Pascal Wehrlein": "de",
    "Daniil Kvyat": "ru",
    "Marcus Ericsson": "se",
    "Jenson Button": "gb",
    "Antonio Giovinazzi": "it",
    "Pierre Gasly": "fr",
    "Robert Kubica": "pl",
    "Charles Leclerc": "mc",
    "Sebastian Buemi": "ch",
    "Brendon Hartley": "nz",
    "Sergey Sirotkin": "ru"}

flagTeamDict = {"Mercedes": "rt_merc",
    "Ferrari": "rt_fer",
    "Red Bull Racing TAG Heuer": "rt_rb",
    "Force India Mercedes": "rt_fi",
    "Williams Mercedes": "rt_wil",
    "Scuderia Toro Rosso Honda": "rt_tor",
    "Renault": "rt_ren",
    "Haas Ferrari": "rt_haas",
    "McLaren Renault": "rt_mcl",
    "Sauber Ferrari": "rt_sau"}

flagTeamDictNat = {"Mercedes": "de",
    "Ferrari": "it",
    "Red Bull Racing TAG Heuer": "at",
    "Force India Mercedes": "in",
    "Williams Mercedes": "gb",
    "Scuderia Toro Rosso Honda": "it",
    "Renault": "fr",
    "Haas Ferrari": "us",
    "McLaren Renault": "gb",
    "Sauber Ferrari": "ch"}
    
barTeamDict = {"Mercedes": "merc",
    "Ferrari": "fer",
    "Red Bull Racing TAG Heuer": "rbr",
    "Force India Mercedes": "sfi",
    "Williams Mercedes": "wil",
    "Scuderia Toro Rosso Honda": "str",
    "Renault": "ren",
    "Haas Ferrari": "has",
    "McLaren Renault": "mcl",
    "Sauber Ferrari": "sau"}

teamShortNameDict = {"Mercedes": "Mercedes",
    "Ferrari": "Ferrari",
    "Red Bull Racing TAG Heuer": "Red Bull Racing",
    "Force India Mercedes": "Force India",
    "Williams Mercedes": "Williams",
    "Scuderia Toro Rosso Honda": "Toro Rosso",
    "Renault": "Renault",
    "Haas Ferrari": "Haas",
    "McLaren Renault": "McLaren",
    "Sauber Ferrari": "Sauber"}
    
teamSubredditDict = {"Mercedes": "[Mercedes](/r/MercedesAMGF1)",
    "Ferrari": "[Ferrari](/r/scuderiaferrari)",
    "Red Bull Racing TAG Heuer": "Red Bull",
    "Force India Mercedes": "[Force India](/r/SaharaForceIndia)",
    "Williams Mercedes": "[Williams](/r/WilliamsF1)",
    "Scuderia Toro Rosso Honda": "[Toro Rosso](/r/ScuderiaToroRosso)",
    "Renault": "Renault",
    "Haas Ferrari": "Haas",
    "McLaren Renault": "McLaren",
    "Sauber Ferrari": "Sauber"}
    
driverSubredditDict = {"Hamilton": "[Hamilton](/r/lewishamilton)",
    "Vettel": "[Vettel](/r/The_Seb)",
    "Bottas": "Bottas",
    "Ricciardo": "Ricciardo",
    "Räikkönen": "[Räikkönen](/r/KimiRaikkonen)",
    "Verstappen": "[Verstappen](/r/maxv)",
    "Perez": "Pérez",
    "Ocon": "[Ocon](/r/EstebanOcon31)",
    "Sainz": "[Sainz](/r/Carlo55ainz)",
    "Hulkenberg": "[Hülkenberg](/r/Hulkenberg)",
    "Massa": "Massa",
    "Stroll": "[Stroll](/r/Lance_Stroll)",
    "Grosjean": "Grosjean",
    "Magnussen": "[Magnussen](/r/KMag20)",
    "Alonso": "[Alonso](/r/The_Fernando)",
    "Palmer": "Palmer",
    "Vandoorne": "[Vandoorne](/r/StoffelWaffle)",
    "Wehrlein": "Wehrlein",
    "Kvyat": "Kvyat",
    "Ericsson": "[Ericsson](/r/MarcusEricsson)",
    "Button": "Button",
    "Giovinazzi": "Giovinazzi",
    "Gasly": "[Gasly](/r/TheGreatGasly)",
    "Kubica": "Kubica",
    "Leclerc": "[Leclerc](/r/CharlesLeclerc)",
    "Buemi": "Buemi",
    "Hartley": "Hartley",
    "Sirotkin": "Sirotkin"}

def raceResults(weekend):
    try:
        address = "https://www.formula1.com/en/results.html/{0}/races/{1}/{2}/race-result.html".format(currentYear, weekend.racenr, weekend.country.lower().replace(" ", "-"))
        page = urllib2.urlopen(address)
        soup = BeautifulSoup(page, "html.parser")
        HTMLtable = soup.find("table", class_="resultsarchive-table").find_all("tr")
        HTMLtitle = soup.find("h1", class_="ResultsArchiveTitle").string
        if not "RACE RESULT" in HTMLtitle:
            return False

        position = []
        racenumber = []
        driver = []
        team = []
        laps = []
        time = []
        points = []

        for idx, line in enumerate(HTMLtable[1:]):
            data = line.find_all(["td", "span"])
            position.append(str(data[1].string))
            racenumber.append(str(data[2].string))
            driver.append("{0} {1}".format(data[4].string, data[5].string))
            team.append(str(data[7].string))
            laps.append(str(data[8].string))
            if(len(data)) == 12:
                time.append(str(data[9].string))
            else:
                time.append("{0}{1}".format(data[9].contents[0], data[9].contents[1].string))
            points.append(str(data[-2].string))

        resultTable = "####Race results\n\n|Pos.|No.|Driver|Team|Laps|Time/Retired|Points|\n|:-:|:-:|:-|:-|:-:|-:|:-:|"
        for i in range(len(position)):
            resultTable += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|".format(position[i], racenumber[i], driver[i], team[i], laps[i], time[i], points[i])

        return resultTable
    except Exception as e:
        print("Error in raceResults: {}".format(e))
        return False

def qualiResults(weekend):
    try:
        address = "https://www.formula1.com/en/results.html/{0}/races/{1}/{2}/qualifying.html".format(currentYear, weekend.racenr, weekend.country.lower().replace(" ", "-"))
        page = urllib2.urlopen(address)
        soup = BeautifulSoup(page, "html.parser")
        HTMLtable = soup.find("table", class_="resultsarchive-table").find_all("tr")
        HTMLtitle = soup.find("h1", class_="ResultsArchiveTitle").string
        if not "QUALIFYING" in HTMLtitle:
            return False

        position = []
        racenumber = []
        driver = []
        team = []
        Q1 = []
        Q2 = []
        Q3 = []
        laps = []

        for idx, line in enumerate(HTMLtable[1:]):
            data = line.find_all(["td", "span"])
            position.append(str(data[1].string))
            racenumber.append(str(data[2].string))
            driver.append("{0} {1}".format(data[4].string, data[5].string))
            team.append(str(data[7].string))
            Q1.append(str(data[8].string))
            if str(data[9].string) == "None":
                Q2.append("")
            else:
                Q2.append(str(data[9].string))
            if str(data[10].string) == "None":
                Q3.append("")
            else:
                Q3.append(str(data[10].string))
            laps.append(str(data[11].string))

        resultTable = "####Qualifying results\n\n|Pos.|No.|Driver|Team|Q1|Q2|Q3|Laps|\n|:-:|:-:|:-|:-|:-|:-|:-|:-|"
        for i in range(len(position)):
            resultTable += "\n|{0}|{1}|{2}|{3}|{4}|{5}|{6}|{7}|".format(position[i], racenumber[i], driver[i], team[i], Q1[i], Q2[i], Q3[i], laps[i])

        return resultTable
    except Exception as e:
        print("Error in qualiResults: {}".format(e))
        return False

def startingGrid(weekend):
    try:
        leftAdd = 0 if weekend.poleLeft else 1
        rightAdd = 1 if weekend.poleLeft else 0
        address = "https://www.formula1.com/en/results.html/{0}/races/{1}/{2}/starting-grid.html".format(currentYear, weekend.racenr, weekend.country.lower().replace(" ", "-"))
        page = urllib2.urlopen(address)
        soup = BeautifulSoup(page, "html.parser")
        HTMLtable = soup.find("table", class_="resultsarchive-table").find_all("tr")
        HTMLtitle = soup.find("h1", class_="ResultsArchiveTitle").string
        if not "STARTING GRID" in HTMLtitle:
            return False
        try:
            HTMLnote = "\n\n" + soup.find("p", class_="note").string
        except Exception as e:
            HTMLnote = ""
        position = []
        racenumber = []
        driver = []
        team = []
        time = []

        for idx, line in enumerate(HTMLtable[1:]):
            data = line.find_all(["td", "span"])
            position.append(str(data[1].string))
            racenumber.append(str(data[2].string))
            driver.append("{0} {1}".format(data[4].string, data[5].string).replace("  ", " "))
            team.append(str(data[7].string))
            time.append(str(data[8].string))

        resultTable = "####Starting grid\n\n|Row|Lane {0}|Lane {1}|\n|-|-|-|".format(1+leftAdd, 1+rightAdd)
        for i in range(int(ceil(len(position)/2))):
            resultTable += "\n|{0}|**{1}.** **[](#{2}) {3}** **{4}** [{5}](#{6})|**{7}.** **[](#{8}) {9}** **{10}** [{11}](#{12})|".format(i+1, position[2*i+leftAdd], flagDriverDict[driver[2*i+leftAdd]], driver[2*i+leftAdd], time[2*i+leftAdd], team[2*i+leftAdd], flagTeamDict[team[2*i+leftAdd]], position[2*i+rightAdd], flagDriverDict[driver[2*i+rightAdd]], driver[2*i+rightAdd], time[2*i+rightAdd], team[2*i+rightAdd], flagTeamDict[team[2*i+rightAdd]])
        resultTable += HTMLnote

        return resultTable
    except Exception as e:
        print("Error in startingGrid: {}".format(e))
        return False

def driverStandings(type=0):
    try:
        address = "https://www.formula1.com/en/results.html/{0}/drivers.html".format(currentYear)
        page = urllib2.urlopen(address)
        soup = BeautifulSoup(page, "html.parser")
        HTMLtable = soup.find("table", class_="resultsarchive-table").find_all("tr")
        
        driver = []
        driverFull = []
        team = []
        points = []
        
        for idx, line in enumerate(HTMLtable[1:]):
            data = line.find_all(["td", "span"])
            driver.append(str(data[4].string))
            driverFull.append("{0} {1}".format(data[3].string, data[4].string).replace("  ", " "))
            team.append(str(data[7].find("a").string))
            points.append(str(data[8].string))
        
        if type == 0:
            resultTable = "\n>|#|Driver • Team|Pts|\n|-|-|-"
            for i in range(10):
                resultTable += "\n|{0:02d}|[](#{1}) {2} • {3}|{4}".format(i+1, flagDriverDict[driverFull[i]], driver[i], teamShortNameDict[team[i]], points[i])
        else:
            resultTable = "\n> \n> |#|Driver|Team|Pts|\n> |:-:|:--|:--|:-:|"
            for i in range(20):
                resultTable += "\n> |{0} [](#{1})|[](#{2}) {3}|{4}|{5}|".format(i+1, barTeamDict[team[i]], flagDriverDict[driverFull[i]], driverSubredditDict[driver[i]], teamSubredditDict[team[i]], points[i])
        return resultTable
        
    except Exception as e:
        print("Error in driverStandings: {}".format(e))

def teamStandings(type=0):
    try:
        address = "https://www.formula1.com/en/results.html/{0}/team.html".format(currentYear)
        page = urllib2.urlopen(address)
        soup = BeautifulSoup(page, "html.parser")
        HTMLtable = soup.find("table", class_="resultsarchive-table").find_all("tr")
        
        team = []
        points = []
        
        for idx, line in enumerate(HTMLtable[1:]):
            data = line.find_all(["td", "span"])
            team.append(str(data[2].find("a").string))
            points.append(str(data[3].string))
        
        if type == 0:
            resultTable = "\n>|#|Team|Pts|\n|-|-|-"
            for i in range(10):
                resultTable += "\n|{0:02d}|[](#{1}) {2}|{3}".format(i+1, flagTeamDictNat[team[i]], team[i], points[i])
        else:
            resultTable = "\n> \n> |#|Team|Pts|\n> |:-:|:--|:-:|"
            for i in range(10):
                resultTable += "\n> |{0} [](#{1})|[](#{2}) {3}|{4}".format(i+1, barTeamDict[team[i]], flagTeamDictNat[team[i]], teamSubredditDict[team[i]], points[i])
        return resultTable
        
    except Exception as e:
        print("Error in teamStandings: {}".format(e))
        return False

def sessionFinished(session):
    global lastQ2Time
    try:
        display = Display(visible=0, size=(800, 600))
        display.start()
        driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
        driver.get("https://www.formula1.com/en/f1-live.html")
        session_name = driver.find_element_by_class_name("SP_chevron").text
        flag = time_left = driver.find_element_by_id("notification").text
        driver.close()
        display.stop()
        if session_name == "LIVE Q2":
            lastQ2Time = datetime.datetime.utcnow()
        if (session == "quali" and session_name == "LIVE Q3" and "CHEQUERED FLAG" in flag) or (session == "race" and (session_name == "RACE" or session_name == "LIVE RACE") and "CHEQUERED FLAG" in flag) or (session == "any" and "CHEQUERED FLAG" in flag):
            text_file = open("{}.txt".format(session_name), "a")
            text_file.write("\n\nsession: {0}\n session_name: {1}\n notification: {2}\n\n".format(session, session_name, flag))
            text_file.close()
            return True
        else:
            return False
    except Exception as e:
        print("Error in sessionFinished: {}".format(e))
        return False