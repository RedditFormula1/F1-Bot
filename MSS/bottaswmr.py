import requests
import arrow
import time
import math
from urllib.parse import urlencode

version = "0.7"

# All times in US/New-York
# Be precise with session title formatting. 
# 'Session title': ['Time in US/NYC', 'Category', 'Length (min']
# Acceptable session titles: 'FP1', 'FP2', 'FP3', 'Practice' 'Qualifying', 'Race', 'F2 Free Practice', 'F2 Qualifying', 'F2 Sprint Race', 'F2 Feature Race', 'F3 Free Practice', 'F3 Qualifying', 'F3 Sprint Race', 'F3 Feature Race'
# Acceptable categories: 'F1', 'F2', 'F3', 'NASCAR'

# added f1, f2, motogp until 2021-05-02
# only used existing session titles

# FOR LATER:
# f2 and f3 (doesnt start until may) have new race formats this season so new titles needed:
# - "F2 Sprint Race 1|2", "F3 Race 1|2|3"
# currently not ideal for motogp:
# - "Friday", "Saturday", "Sunday" is what I used last year
# -> could even be reduced to just a single event per weekend because nearly all streams links will be the same full day coverage anyway
# - the start time now is the first session (any class) of day

sessions = {
    'FP1 - Bahrain Grand Prix': ['2021-03-26 07:30', 'F1', '90'],
    'FP2 - Bahrain Grand Prix': ['2021-03-26 11:00', 'F1', '90'],
    'FP3 - Bahrain Grand Prix': ['2021-03-27 08:00', 'F1', '60'],
    'Qualifying - Bahrain Grand Prix': ['2021-03-27 11:00', 'F1', '60'],
    'Race - Bahrain Grand Prix': ['2021-03-28 11:00', 'F1', '120'],
    'FP1 - Emilia Romagna Grand Prix': ['2021-04-16 05:30', 'F1', '90'],
    'FP2 - Emilia Romagna Grand Prix': ['2021-04-16 09:00', 'F1', '90'],
    'FP3 - Emilia Romagna Grand Prix': ['2021-04-17 06:00', 'F1', '60'],
    'Qualifying - Emilia Romagna Grand Prix': ['2021-04-17 09:00', 'F1', '60'],
    'Race - Emilia Romagna Grand Prix': ['2021-04-18 09:00', 'F1', '120'],
    'FP1 - Portuguese Grand Prix': ['2021-04-30 07:30', 'F1', '90'],
    'FP2 - Portuguese Grand Prix': ['2021-04-30 11:00', 'F1', '90'],
    'FP3 - Portuguese Grand Prix': ['2021-05-01 08:00', 'F1', '60'],
    'Qualifying - Portuguese Grand Prix': ['2021-05-01 11:00', 'F1', '60'],
    'Race - Portuguese Grand Prix': ['2021-05-02 11:00', 'F1', '120'],
    'F2 Free Practice - Sakhir': ['2021-03-26 06:05', 'F2', '45'],
    'F2 Qualifying - Sakhir': ['2021-03-26 09:30', 'F2', '30'],
    'F2 Sprint Race - Sakhir 1': ['2021-03-27 06:25', 'F2', '45'],
    'F2 Sprint Race - Sakhir 2': ['2021-03-27 12:40', 'F2', '45'],
    'F2 Feature Race - Sakhir': ['2021-03-28 06:50', 'F2', '60'],
    'Practice - Grand Prix of Qatar': ['2021-03-26 06:50', 'MotoGP', '600'],
    'Qualifying - Grand Prix of Qatar': ['2021-03-27 06:25', 'MotoGP', '600'],
    'Race - Grand Prix of Qatar': ['2021-03-28 07:40', 'MotoGP', '600'],
    'Practice - Grand Prix of Doha': ['2021-04-02 06:50', 'MotoGP', '600'],
    'Qualifying - Grand Prix of Doha': ['2021-04-03 06:25', 'MotoGP', '600'],
    'Race - Grand Prix of Doha': ['2021-04-04 07:40', 'MotoGP', '600'],
    'Practice - Portugese Grand Prix': ['2021-04-16 04:00', 'MotoGP', '600'],
    'Qualifying - Portugese Grand Prix': ['2021-04-17 04:00', 'MotoGP', '600'],
    'Race - Portugese Grand Prix': ['2021-04-18 04:00', 'MotoGP', '600'],
    'Practice - Spanish Grand Prix': ['2021-04-30 03:00', 'MotoGP', '600'],
    'Qualifying - Spanish Grand Prix': ['2021-05-01 03:00', 'MotoGP', '600'],
    'Race - Spanish Grand Prix': ['2021-05-02 02:20', 'MotoGP', '600']
    
}

cover_images = {
    "FP1": "https://i.imgur.com/qwpMftT.png",
    "FP2": "https://i.imgur.com/nGlULND.png",
    "FP3": "https://i.imgur.com/ewFOtB8.png",
    "Practice": "https://i.imgur.com/lYjKLXu.png",
    "Qualifying": "https://i.imgur.com/1jmj9DO.png",
    "Race": "https://i.imgur.com/ovif4aj.png",
    "F2 Free Practice": "https://i.imgur.com/hnHko8q.png",
    "F2 Qualifying": "https://i.imgur.com/1jmj9DO.png",
    "F2 Sprint Race": "https://i.imgur.com/ndcVdZu.png",
    "F2 Feature Race": "https://i.imgur.com/PwwcFiW.png",
    "F3 Free Practice": "https://i.imgur.com/hnHko8q.png",
    "F3 Qualifying": "https://i.imgur.com/1jmj9DO.png",
    "F3 Sprint Race": "https://i.imgur.com/ndcVdZu.png",
    "F3 Feature Race": "https://i.imgur.com/PwwcFiW.png",
}

groups = {
    "F1": 13,
    "F2": 76,
    "F3": 77,
    "NASCAR": 78,
    "MotoGP": 72,
}

# Delay until sessions are available to streamers (seconds)
# 43200 = 12 hours
create_delay = 86400

# Delay until sessions are published for viewing (seconds)
# 3600 = 1 hours
publish_delay = 7200

# Delay to delete sessions after they begin (seconds, negative, deprecated) 
# 3600 = 1 hours
# remove_delay = -10800


sportsurge_token = "aqiCZUO2STd3uEbU4x6Y5xwGHPlBxRFcQS7WM8ASWbRRiGnO"

sportsurge_base_url = "https://api.sportsurge.net"

cache_submitted = []
cache_published = []

def submit_game(session):
    session_time = sessions[session][0]

    start_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").timestamp

    post_title = session

    london_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Europe/London")

    ny_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York")

    london_string = london_time.format("dddd, MMMM D - h:mma")

    sydney_string = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Australia/Sydney").format("h:mma")

    tokyo_string = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Asia/Tokyo").format("h:mma")

    ny_string = ny_time.format("h:mma")

    print("Submitting " + post_title + "...")

    group = groups[sessions[session][1]]

    try:
        cover_image = cover_images[post_title.split(' - ')[0]]
    except:
        cover_image = None

    post_req = requests.post(sportsurge_base_url + "/events/single", headers={"Authorization": "Bearer " + sportsurge_token}, json={
        "name": post_title,
        "group": group,
        "status": 0,
        "imageURL": cover_image,
        "description": london_string + " London / " + ny_string + " NYC / " + sydney_string + " Sydney / " + tokyo_string + " Tokyo",
        "date": start_time
    })

    if post_req.status_code == 201:
        print("Submitted " + post_title + "!")
        cache_submitted.append(session)
    else:
        print("FAILED " + post_title + "! (" + str(post_req.status_code) + ")")

def publish_game(session):
    title = session
    print("Publishing (" + title + ")...")
    pub_req = requests.patch(sportsurge_base_url + "/events/single/publish?event=" + str(check_for_submission(title)), headers={"Authorization": "Bearer " + sportsurge_token})

    if pub_req.status_code == 200:
        print("Published " + title + "!")
        cache_published.append(session)
    else:
        print("FAILED publishing " + title + "!")

def remove_game(game, session):
    print("Removing " + str(session) + " (" + str(game) + ")...")
    del_req = requests.delete(sportsurge_base_url + "/events/single?event=" + str(game), headers={"Authorization": "Bearer " + sportsurge_token})

    if del_req.status_code == 200:
        print("Deleted " + str(session) + ".")
        # if session_time in cache_submitted:
        #     cache_submitted.remove(session_time)
        # if session_time in cache_published:
        #     cache_published.remove(session_time)
    else:
        print("FAILED DELETING " + str(session) + "!")

def generate_thread_title(session):
    return session

def check_for_submission(title):
    api_url = sportsurge_base_url + "/events/singletitle?" + urlencode({"title": title})
    req = requests.get(api_url)
    if req.status_code == 200:
        # Event exists
        return req.json()["id"]
    else:
        return False

def get_games():
    print("Managing Sportsurge")
    utc = arrow.utcnow()
    eastern = utc.to("US/Eastern")
    current_time = arrow.utcnow()

    for session in sessions.keys():
        seconds_until_event = arrow.get(sessions[session][0], "YYYY-MM-DD HH:mm", tzinfo="US/Eastern").timestamp - int(current_time.format("X"))
        remove_delay = (-1 * ((int(sessions[session][2]) * 60) + 3600))

        if seconds_until_event <= create_delay and seconds_until_event > 0 and session not in cache_submitted:
            if check_for_submission(generate_thread_title(session)) == False:
                submit_game(session)

        # Publishing the event
        if seconds_until_event <= publish_delay and seconds_until_event > 0 and session not in cache_published:
            publish_game(session)

        # Removing the event
        elif seconds_until_event <= remove_delay and (remove_delay - seconds_until_event) < 3600:
            posted_game = check_for_submission(generate_thread_title(session))
            if posted_game != False:
                remove_game(posted_game, session)


    #print("Completed operation. Sleeping...")
    #time.sleep(500)
    #get_games()

 #print("Starting MotorsportStreams bot v" + version + "!")
#get_games()
