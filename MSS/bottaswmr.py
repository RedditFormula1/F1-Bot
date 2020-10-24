import requests
import arrow
import time
import math
from urllib.parse import urlencode

version = "0.6"

# All times in US/New-York
# Be precise with session title formatting. 
# 'Session title': ['Time in US/NYC', 'Category', 'Length (min']
# Acceptable session titles" 'FP1', 'FP2', 'FP3', 'Qualifying', 'Race', 'F2 Free Practice', 'F2 Qualifying', 'F2 Sprint Race', 'F2 Feature Race', 'F3 Free Practice', 'F3 Qualifying', 'F3 Sprint Race', 'F3 Feature Race'

sessions = {
    'FP1 - Austrian Grand Prix': ['2020-07-03 05:00', 'F1', '90'],
    'FP2 - Austrian Grand Prix': ['2020-07-03 09:00', 'F1', '90'],
    'FP3 - Austrian Grand Prix': ['2020-07-04 06:00', 'F1', '60'],
    'Qualifying - Austrian Grand Prix': ['2020-07-04 09:00', 'F1', '60'],
    'Race - Austrian Grand Prix': ['2020-07-05 09:10', 'F1', '120'],
    'FP1 - Styrian Grand Prix': ['2020-07-10 05:00', 'F1', '90'],
    'FP2 - Styrian Grand Prix': ['2020-07-10 09:00', 'F1', '90'],
    'FP3 - Styrian Grand Prix': ['2020-07-11 06:00', 'F1', '60'],
    'Qualifying - Styrian Grand Prix': ['2020-07-11 09:00', 'F1', '60'],
    'Race - Styrian Grand Prix': ['2020-07-12 09:10', 'F1', '120'],
    'FP1 - Hungarian Grand Prix': ['2020-07-17 05:00', 'F1', '90'],
    'FP2 - Hungarian Grand Prix': ['2020-07-17 09:00', 'F1', '90'],
    'FP3 - Hungarian Grand Prix': ['2020-07-18 06:00', 'F1', '60'],
    'Qualifying - Hungarian Grand Prix': ['2020-07-18 09:00', 'F1', '60'],
    'Race - Hungarian Grand Prix': ['2020-07-19 09:10', 'F1', '120'],
    'FP1 - British Grand Prix': ['2020-07-31 06:00', 'F1', '90'],
    'FP2 - British Grand Prix': ['2020-07-31 10:00', 'F1', '90'],
    'FP3 - British Grand Prix': ['2020-08-01 06:00', 'F1', '60'],
    'Qualifying - British Grand Prix': ['2020-08-01 09:00', 'F1', '60'],
    'Race - British Grand Prix': ['2020-08-02 09:10', 'F1', '120'],
    'FP1 - 70th Anniversary Grand Prix': ['2020-08-07 06:00', 'F1', '90'],
    'FP2 - 70th Anniversary Grand Prix': ['2020-08-07 10:00', 'F1', '90'],
    'FP3 - 70th Anniversary Grand Prix': ['2020-08-08 06:00', 'F1', '60'],
    'Qualifying - 70th Anniversary Grand Prix': ['2020-08-08 09:00', 'F1', '60'],
    'Race - 70th Anniversary Grand Prix': ['2020-08-09 09:10', 'F1', '120'],
    'FP1 - Spanish Grand Prix': ['2020-08-14 05:00', 'F1', '90'],
    'FP2 - Spanish Grand Prix': ['2020-08-14 09:00', 'F1', '90'],
    'FP3 - Spanish Grand Prix': ['2020-08-15 06:00', 'F1', '60'],
    'Qualifying - Spanish Grand Prix': ['2020-08-15 09:00', 'F1', '60'],
    'Race - Spanish Grand Prix': ['2020-08-16 09:10', 'F1', '120'],
    'FP1 - Belgian Grand Prix': ['2020-08-28 05:00', 'F1', '90'],
    'FP2 - Belgian Grand Prix': ['2020-08-28 09:00', 'F1', '90'],
    'FP3 - Belgian Grand Prix': ['2020-08-29 06:00', 'F1', '60'],
    'Qualifying - Belgian Grand Prix': ['2020-08-29 09:00', 'F1', '60'],
    'Race - Belgian Grand Prix': ['2020-08-30 09:10', 'F1', '120'],
    'FP1 - Italian Grand Prix': ['2020-09-04 05:00', 'F1', '90'],
    'FP2 - Italian Grand Prix': ['2020-09-04 09:00', 'F1', '90'],
    'FP3 - Italian Grand Prix': ['2020-09-05 06:00', 'F1', '60'],
    'Qualifying - Italian Grand Prix': ['2020-09-05 09:00', 'F1', '60'],
    'Race - Italian Grand Prix': ['2020-09-06 09:10', 'F1', '120'],
    'FP1 - Tuscan Grand Prix': ['2020-09-11 05:00', 'F1', '90'],
    'FP2 - Tuscan Grand Prix': ['2020-09-11 09:00', 'F1', '90'],
    'FP3 - Tuscan Grand Prix': ['2020-09-12 06:00', 'F1', '60'],
    'Qualifying - Tuscan Grand Prix': ['2020-09-12 09:00', 'F1', '60'],
    'Race - Tuscan Grand Prix': ['2020-09-13 09:10', 'F1', '120'],
    'FP1 - Russian Grand Prix': ['2020-09-24 04:00', 'F1', '90'],
    'FP2 - Russian Grand Prix': ['2020-09-24 08:00', 'F1', '90'],
    'FP3 - Russian Grand Prix': ['2020-09-25 05:00', 'F1', '60'],
    'Qualifying - Russian Grand Prix': ['2020-09-25 08:00', 'F1', '60'],
    'Race - Russian Grand Prix': ['2020-09-27 07:10', 'F1', '120'],
    'FP1 - Portuguese Grand Prix': ['2020-10-23 06:00', 'F1', '90'],
    'FP2 - Portuguese Grand Prix': ['2020-10-23 10:00', 'F1', '90'],
    'FP3 - Portuguese Grand Prix': ['2020-10-24 06:00', 'F1', '60'],
    'Qualifying - Portuguese Grand Prix': ['2020-10-24 09:00', 'F1', '60'],
    'Race - Portuguese Grand Prix': ['2020-10-25 09:10', 'F1', '120'],
    'FP1 - Eifel Grand Prix': ['2020-10-09 05:00', 'F1', '90'],
    'FP2 - Eifel Grand Prix': ['2020-10-09 09:00', 'F1', '90'],
    'FP3 - Eifel Grand Prix': ['2020-10-10 06:00', 'F1', '60'],
    'Qualifying - Eifel Grand Prix': ['2020-10-10 09:00', 'F1', '60'],
    'Race - Eifel Grand Prix': ['2020-10-11 08:10', 'F1', '120'],
    'F2 Free Practice - Spain': ['2020-08-14 06:55', 'F2', '45'],
    'F2 Qualifying - Tuscany': ['2020-09-11 10:55', 'F2', '30'],
    'F2 Feature Race - Britain': ['2020-08-08 10:45', 'F2', '60'],
    'F2 Feature Race - Spain': ['2020-08-15 10:45', 'F2', '60'],
    'F2 Free Practice - Tuscany': ['2020-09-11 07:00', 'F2', '45'],
    'F2 Qualifying - Spain': ['2020-08-14 11:00', 'F2', '30'],
    'F2 Feature Race - Russia': ['2020-09-26 09:45', 'F2', '60'],
    'F2 Qualifying - Russia': ['2020-09-25 10:00', 'F2', '30'],
    'F2 Free Practice - Belgium': ['2020-08-28 06:55', 'F2', '45'],
    'F2 Sprint Race - Tuscany': ['2020-09-13 04:50', 'F2', '45'],
    'F2 Qualifying - Britain': ['2020-08-07 12:00', 'F2', '30'],
    'F2 Free Practice - Russia': ['2020-09-25 02:30', 'F2', '45'],
    'F2 Qualifying - Belgium': ['2020-08-28 11:00', 'F2', '30'],
    'F2 Sprint Race - Italy': ['2020-09-06 04:50', 'F2', '45'],
    'F2 Feature Race - Tuscany': ['2020-09-12 10:45', 'F2', '60'],
    'F2 Sprint Race - Belgium': ['2020-08-30 05:10', 'F2', '45'],
    'F2 Sprint Race - Britain': ['2020-08-09 05:10', 'F2', '45'],
    'F2 Feature Race - Italy': ['2020-09-05 10:45', 'F2', '60'],
    'F2 Free Practice - Italy': ['2020-09-04 07:00', 'F2', '45'],
    'F2 Sprint Race - Russia': ['2020-09-27 04:20', 'F2', '45'],
    'F2 Sprint Race - Spain': ['2020-08-16 05:10', 'F2', '45'],
    'F2 Free Practice - Britain': ['2020-08-07 07:55', 'F2', '45'],
    'F2 Qualifying - Italy': ['2020-09-04 10:55', 'F2', '30'],
    'F2 Feature Race - Belgium': ['2020-08-29 10:45', 'F2', '60'],
    'F3 Sprint Race - Italy': ['2020-09-06 03:45', 'F3', '40'],
    'F3 Sprint Race - Tuscany': ['2020-09-13 03:45', 'F3', '40'],
    'F3 Free Practice - Belgium': ['2020-08-28 03:35', 'F3', '45'],
    'F3 Sprint Race - Spain': ['2020-08-16 03:45', 'F3', '40'],
    'F3 Qualifying - Spain': ['2020-08-14 08:05', 'F3', '30'],
    'F3 Qualifying - Britain': ['2020-08-07 09:05', 'F3', '30'],
    'F3 Feature Race - Italy': ['2020-09-05 04:25', 'F3', '40'],
    'F3 Free Practice - Spain': ['2020-08-14 03:35', 'F3', '45'],
    'F3 Sprint Race - Belgium': ['2020-08-30 03:45', 'F3', '40'],
    'F3 Free Practice - Italy': ['2020-09-04 03:35', 'F3', '45'],
    'F3 Sprint Race - Britain': ['2020-08-02 03:45', 'F3', '40'],
    'F3 Feature Race - Belgium': ['2020-08-29 04:25', 'F3', '40'],
    'F3 Free Practice - Tuscany': ['2020-09-11 03:35', 'F3', '45'],
    'F3 Feature Race - Britain': ['2020-08-08 04:25', 'F3', '40'],
    'F3 Qualifying - Tuscany': ['2020-09-11 08:05', 'F3', '30'],
    'F3 Free Practice - Britain': ['2020-08-07 04:35', 'F3', '45'],
    'F3 Qualifying - Belgium': ['2020-08-28 08:05', 'F3', '30'],
    'F3 Qualifying - Italy': ['2020-09-04 08:05', 'F3', '30'],
    'F3 Feature Race - Spain': ['2020-08-15 04:25', 'F3', '40'],
    'F3 Feature Race - Tuscany': ['2020-09-12 04:25', 'F3', '40'],
    'FP1 - Emilia Romagna Grand Prix': ['2020-10-31 05:00', 'F1', '90'],
    'Qualifying - Emilia Romagna Grand Prix': ['2020-10-31 09:00', 'F1', '60'],
    'Race - Emilia Romagna Grand Prix': ['2020-11-01 07:10', 'F1', '120'],
    'FP1 - Turkish Grand Prix': ['2020-11-13 03:00', 'F1', '90'],
    'FP2 - Turkish Grand Prix': ['2020-11-13 07:00', 'F1', '90'],
    'FP3 - Turkish Grand Prix': ['2020-11-14 04:00', 'F1', '60'],
    'Qualifying - Turkish Grand Prix': ['2020-11-14 07:00', 'F1', '60'],
    'Race - Turkish Grand Prix': ['2020-11-15 05:10', 'F1', '120'],
    'FP1 - Bahrain Grand Prix': ['2020-11-27 06:00', 'F1', '90'],
    'FP2 - Bahrain Grand Prix': ['2020-11-27 10:00', 'F1', '90'],
    'FP3 - Bahrain Grand Prix': ['2020-11-28 07:00', 'F1', '60'],
    'Qualifying - Bahrain Grand Prix': ['2020-11-28 10:00', 'F1', '60'],
    'Race - Bahrain Grand Prix': ['2020-11-29 10:10', 'F1', '120'],
    'FP1 - Sakhir Grand Prix': ['2020-12-04 08:30', 'F1', '90'],
    'FP2 - Sakhir Grand Prix': ['2020-12-04 12:30', 'F1', '90'],
    'FP3 - Sakhir Grand Prix': ['2020-12-05 10:00', 'F1', '60'],
    'Qualifying - Sakhir Grand Prix': ['2020-12-05 13:00', 'F1', '60'],
    'Race - Sakhir Grand Prix': ['2020-12-06 12:10', 'F1', '120'],
    'FP1 - Abu Dhabi Grand Prix': ['2020-12-11 04:00', 'F1', '90'],
    'FP2 - Abu Dhabi Grand Prix': ['2020-12-11 08:00', 'F1', '90'],
    'FP3 - Abu Dhabi Grand Prix': ['2020-12-12 05:00', 'F1', '60'],
    'Qualifying - Abu Dhabi Grand Prix': ['2020-12-12 08:00', 'F1', '60'],
    'Race - Abu Dhabi Grand Prix': ['2020-12-13 08:10', 'F1', '120']
    
}

cover_images = {
    "FP1": "https://i.imgur.com/qwpMftT.png",
    "FP2": "https://i.imgur.com/nGlULND.png",
    "FP3": "https://i.imgur.com/ewFOtB8.png",
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


    print("Completed operation. Sleeping...")
    time.sleep(500)
    get_games()

 #print("Starting MotorsportStreams bot v" + version + "!")
get_games()
