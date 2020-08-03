import requests
import arrow
import time
import math
from urllib.parse import urlencode

version = "0.4"

sessions = {
    "2020-07-03 05:00": "FP1 - Austrian Grand Prix",
    "2020-07-03 09:00": "FP2 - Austrian Grand Prix",
    "2020-07-04 06:00": "FP3 - Austrian Grand Prix",
    "2020-07-04 09:00": "Qualifying - Austrian Grand Prix",
    "2020-07-05 09:10": "Race - Austrian Grand Prix",
    "2020-07-10 05:00": "FP1 - Styrian Grand Prix",
    "2020-07-10 09:00": "FP2 - Styrian Grand Prix",
    "2020-07-11 06:00": "FP3 - Styrian Grand Prix",
    "2020-07-11 09:00": "Qualifying - Styrian Grand Prix",
    "2020-07-12 09:10": "Race - Styrian Grand Prix",
    "2020-07-17 05:00": "FP1 - Hungarian Grand Prix",
    "2020-07-17 09:00": "FP2 - Hungarian Grand Prix",
    "2020-07-18 06:00": "FP3 - Hungarian Grand Prix",
    "2020-07-18 09:00": "Qualifying - Hungarian Grand Prix",
    "2020-07-19 09:10": "Race - Hungarian Grand Prix",
    "2020-07-31 06:00": "FP1 - British Grand Prix",
    "2020-07-31 10:00": "FP2 - British Grand Prix",
    "2020-08-01 06:00": "FP3 - British Grand Prix",
    "2020-08-01 09:00": "Qualifying - British Grand Prix",
    "2020-08-02 09:10": "Race - British Grand Prix",
    "2020-08-07 06:00": "FP1 - 70th Anniversary Grand Prix",
    "2020-08-07 10:00": "FP2 - 70th Anniversary Grand Prix",
    "2020-08-08 06:00": "FP3 - 70th Anniversary Grand Prix",
    "2020-08-08 09:00": "Qualifying - 70th Anniversary Grand Prix",
    "2020-08-09 09:10": "Race - 70th Anniversary Grand Prix",
    "2020-08-14 05:00": "FP1 - Spanish Grand Prix",
    "2020-08-14 09:00": "FP2 - Spanish Grand Prix",
    "2020-08-15 06:00": "FP3 - Spanish Grand Prix",
    "2020-08-15 09:00": "Qualifying - Spanish Grand Prix",
    "2020-08-16 09:10": "Race - Spanish Grand Prix",
    "2020-08-28 05:00": "FP1 - Belgian Grand Prix",
    "2020-08-28 09:00": "FP2 - Belgian Grand Prix",
    "2020-08-29 06:00": "FP3 - Belgian Grand Prix",
    "2020-08-29 09:00": "Qualifying - Belgian Grand Prix",
    "2020-08-30 09:10": "Race - Belgian Grand Prix",
    "2020-09-04 05:00": "FP1 - Italian Grand Prix",
    "2020-09-04 09:00": "FP2 - Italian Grand Prix",
    "2020-09-05 06:00": "FP3 - Italian Grand Prix",
    "2020-09-05 09:00": "Qualifying - Italian Grand Prix",
    "2020-09-06 09:10": "Race - Italian Grand Prix",
    "2020-09-11 05:00": "FP1 - Tuscan Grand Prix",
    "2020-09-11 09:00": "FP2 - Tuscan Grand Prix",
    "2020-09-12 06:00": "FP3 - Tuscan Grand Prix",
    "2020-09-12 09:00": "Qualifying - Tuscan Grand Prix",
    "2020-09-13 09:10": "Race - Tuscan Grand Prix",
    "2020-09-11 04:00": "FP1 - Russian Grand Prix",
    "2020-09-11 08:00": "FP2 - Russian Grand Prix",
    "2020-09-12 05:00": "FP3 - Russian Grand Prix",
    "2020-09-12 08:00": "Qualifying - Russian Grand Prix",
    "2020-09-13 07:10": "Race - Russian Grand Prix",
}
# Delay until sessions are available to streamers (seconds)
# 43200 = 12 hours
create_delay = 86400

# Delay until sessions are published for viewing (seconds)
# 3600 = 1 hours
publish_delay = 7200

# Delay to delete sessions after they being (seconds, negative) 
# 3600 = 1 hours
remove_delay = -10800


sportsurge_token = "aqiCZUO2STd3uEbU4x6Y5xwGHPlBxRFcQS7WM8ASWbRRiGnO"

sportsurge_base_url = "https://api.sportsurge.net"

group = 13

cache_submitted = []
cache_published = []

def submit_game(session_time):
    start_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").timestamp

    post_title = sessions[session_time]

    london_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Europe/London")

    ny_time = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York")

    london_string = london_time.format("dddd, MMMM D - h:mma")

    sydney_string = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Australia/Sydney").format("h:mma")

    tokyo_string = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="America/New_York").to("Asia/Tokyo").format("h:mma")

    ny_string = ny_time.format("h:mma")

    print("Submitting " + post_title + "...")

    post_req = requests.post(sportsurge_base_url + "/events/single", headers={"Authorization": "Bearer " + sportsurge_token}, json={
        "name": post_title,
        "group": group,
        "status": 0,
        "imageURL": "https://i.imgur.com/NpvBiG9.png",
        "description": london_string + " London / " + ny_string + " NYC / " + sydney_string + " Sydney / " + tokyo_string + " Tokyo",
        "date": start_time
    })

    if post_req.status_code == 201:
        print("Submitted " + post_title + "!")
        cache_submitted.append(session_time)
    else:
        print("FAILED " + post_title + "! (" + str(post_req.status_code) + ")")

def publish_game(session_time):
    title = sessions[session_time]
    print("Publishing (" + title + ")...")
    pub_req = requests.patch(sportsurge_base_url + "/events/single/publish?event=" + str(check_for_submission(title)), headers={"Authorization": "Bearer " + sportsurge_token})

    if pub_req.status_code == 200:
        print("Published " + title + "!")
        cache_published.append(session_time)
    else:
        print("FAILED publishing " + title + "!")

def remove_game(game, session_time):
    print("Removing " + str(session_time) + "(" + str(generate_thread_title(session_time)) + ")...")
    del_req = requests.delete(sportsurge_base_url + "/events/single?event=" + str(game), headers={"Authorization": "Bearer " + sportsurge_token})

    if del_req.status_code == 200:
        print("Deleted " + str(game) + ".")
        # if session_time in cache_submitted:
        #     cache_submitted.remove(session_time)
        # if session_time in cache_published:
        #     cache_published.remove(session_time)
    else:
        print("FAILED DELETING " + str(game) + "!")

def generate_thread_title(session_time):
    return sessions[session_time]

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

    for session_time in sessions.keys():
        seconds_until_event = arrow.get(session_time, "YYYY-MM-DD HH:mm", tzinfo="US/Eastern").timestamp - int(current_time.format("X"))

        if seconds_until_event <= create_delay and seconds_until_event > 0 and session_time not in cache_submitted:
            if check_for_submission(generate_thread_title(session_time)) == False:
                submit_game(session_time)

        # Publishing the event
        if seconds_until_event <= publish_delay and seconds_until_event > 0 and session_time not in cache_published:
            publish_game(session_time)

        # Removing the event
        elif seconds_until_event <= remove_delay and (remove_delay - seconds_until_event) < 3600:
            print(remove_delay - seconds_until_event)
            posted_game = check_for_submission(generate_thread_title(session_time))
            print(generate_thread_title)
            print(posted_game)
            if posted_game != False:
                remove_game(posted_game, session_time)

    print("Completed operation. Sleeping...")
    time.sleep(500)
    get_games()

#print("Starting MotorsportStreams bot v" + version + "!")

