#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
22 Mar 2018
"""

hub_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"| Session | UTC | Weather prediction|\n"\
"| - | - | - |\n| Free Practice 1 | {3} | []({4}) {5}, {6} °C / {7} °F|\n"\
"| Free Practice 2 | {8} | []({9}) {10}, {11} °C / {12} °F|\n"\
"| Free Practice 3 | {13} | []({14}) {15}, {16} °C / {17} °F|\n"\
"| Qualifying | {18} | []({19}) {20}, {21} °C / {22} °F|\n"\
"| Race | {23} | []({24}) {25}, {26} °C / {27} °F|\n"\
"\n"\
"[Click here](http://f1calendar.com/) for start times in your area.\n"\
"\n"\
"Please note that this weather prediction does not get updated. For an up-to-date weather prediction, see the sidebar.\n"\
"\n"\
"---\n"\
"\n"\
"#### Threads\n"\
"\n"\
"**Sessions**[](/sessionsBegin)\n"\
"\n"\
" - No links yet[](/sessionsEnd)\n"\
"\n"\
"**Extras**\n"\
"\n"\
" - No links yet\n"\
"\n"\
"####IRC Chat\n"\
"\n"\
"Join us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n"\
"\n"\
"Stream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n"\
"\n"\
"Be sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.\n"\
"\n"\
"---\n"\
"\n"\
"####F1 Fantasy League\n"\
"\n"\
"Remember to update your F1 Fantasy team. Join the [official subreddit league here](https://fantasy.formula1.com/join/?=a3b1ff4e8b), or use invite code `a3b1ff4e8b`."

old_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {42} |\n"\
"| Free Practice 2 | {43} |\n"\
"| Free Practice 3 | {44} |\n"\
"| Qualifying | {11} |\n"\
"| Race | {12} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {13}\n"\
"\n"\
"**Length:** {14} km ({15:.3f} mi)\n"\
"\n"\
"**Distance:** {16} laps, {17} km ({18:.3f} mi)\n"\
"\n"\
"**Lap record:** []({19}) {20}, {21}, {22}, {23}\n"\
"\n"\
"**{24} pole:** []({25}) {26}, {27}, {28}\n"\
"\n"\
"**{29} fastest lap:** []({30}) {31}, {32}, {33}\n"\
"\n"\
"**{34} winner:** []({35}) {36}, {37}\n"\
"\n"\
"{45}---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n- Wiki: [Race]({39}) | [{40}]({41})\n"\
"\n"\
"---\n"\
"\n"\
"#### Streaming & Downloads\n"\
"\n"\
"For information on streams, please visit /r/MotorSportsStreams. Please do not post information about streams in this thread. Thank you.\n"\
"\n"\
"---\n"\
"\n"\
"####Live timing leaderboard\n"\
"\n"\
"For those of you who are F1 ACCESS members, you can check the position of the drivers throughout the race on the [official live timing leaderboard](https://www.formula1.com/en/f1-live.html)\n"\
"\n"\
"---\n"\
"\n"\
"#### Race Discussion\n"\
"\n"\
"Join us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n"\
"\n"\
"Stream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n"\
"\n"\
"Be sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.\n"\
"\n"\
"---\n"\
"\n"\
"####F1 Fantasy League\n"\
"\n"\
"Remember to update your F1 Fantasy team. Join the [official subreddit league here](https://fantasy.formula1.com/join/?=a3b1ff4e8b), or use invite code `a3b1ff4e8b`."

new_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {42} |\n"\
"| Free Practice 2 | {43} |\n"\
"| Free Practice 3 | {44} |\n"\
"| Qualifying | {11} |\n"\
"| Race | {12} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {13}\n"\
"\n"\
"**Length:** {14} km ({15:.3f} mi)\n"\
"\n"\
"**Distance:** {16} laps, {17} km ({18:.3f} mi)\n"\
"\n"\
"**Lap record:** []({19}) {20}, {21}, {22}, {23}\n"\
"\n"\
"**{24} pole:** []({25}) {26}, {27}, {28}\n"\
"\n"\
"**{29} fastest lap:** []({30}) {31}, {32}, {33}\n"\
"\n"\
"**{34} winner:** []({35}) {36}, {37}\n"\
"\n"\
"{45}---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n- Wiki: [Race]({39}) | [{40}]({41})\n"\
"\n"\
"---\n"\
"\n"\
"#### Streaming & Downloads\n"\
"\n"\
"For information on streams, please visit /r/MotorSportsStreams. Please do not post information about streams in this thread. Thank you.\n"\
"\n"\
"---\n"\
"\n"\
"####Live timing leaderboard\n"\
"\n"\
"For those of you who are F1 ACCESS members, you can check the position of the drivers throughout the race on the [official live timing leaderboard](https://www.formula1.com/en/f1-live.html)\n"\
"\n"\
"---\n"\
"\n"\
"#### Race Discussion\n"\
"\n"\
"Join us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n"\
"\n"\
"Stream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n"\
"\n"\
"Be sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.\n"\
"\n"\
"---\n"\
"\n"\
"####F1 Fantasy League\n"\
"\n"\
"Remember to update your F1 Fantasy team. Join the [official subreddit league here](https://fantasy.formula1.com/join/?=a3b1ff4e8b), or use invite code `a3b1ff4e8b`."

post_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {42} |\n"\
"| Free Practice 2 | {43} |\n"\
"| Free Practice 3 | {44} |\n"\
"| Qualifying | {11} |\n"\
"| Race | {12} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {13}\n"\
"\n"\
"**Length:** {14} km ({15:.3f} mi)\n"\
"\n"\
"**Distance:** {16} laps, {17} km ({18:.3f} mi)\n"\
"\n"\
"**Lap record:** []({19}) {20}, {21}, {22}, {23}\n"\
"\n"\
"**{24} pole:** []({25}) {26}, {27}, {28}\n"\
"\n"\
"**{29} fastest lap:** []({30}) {31}, {32}, {33}\n"\
"\n"\
"**{34} winner:** []({35}) {36}, {37}\n"\
"\n"\
"[](/resultsBegin)[](/resultsEnd)\n"\
"\n"\
"---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({38}.html) | [Full Timetable]({38}/Timetable.html)\n"\
"- Wiki: [Race]({39}) | [{40}]({41})\n"\
"\n"\
"---\n"\
"\n"\
"#### Streaming & Downloads\n"\
"\n"\
"For information on downloads, please visit /r/MotorSportsReplays. Please do not post information about downloads in this thread. Thank you."

dad_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"---\n"\
"\n"\
"####Welcome to the Day after Debrief discussion thread!\n"\
"\n"\
"Now that the dust has settled in {3}, it's time to calmly discuss the events of the last race weekend. Hopefully, this will foster more detailed and thoughtful discussion than the immediate post race thread now that people have had some time to digest and analyse the results.\n"\
"\n"\
"Low effort comments, such as memes, jokes, and complaints about broadcasters will be deleted. We also discourage superficial comments that contain no analysis or reasoning in this thread (e.g., 'Great race from X!', 'Another terrible weekend for Y!').\n"\
"\n"\
"Thanks!"

mh_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"---\n"\
"\n"\
"####Highlights:\n"\
"\n"\
"{3}\n"\
"\n"\
"---\n"\
"\n"\
"####Post-Race Interviews:\n"\
"\n"\
"{4}"
