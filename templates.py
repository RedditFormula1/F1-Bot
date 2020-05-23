#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/Redbiertje
22 Mar 2018
"""

lastyear_template = "**Lap record:** []({0}) {1}, {2}, {3}, {4}\n"\
"\n"\
"**{5} pole:** []({6}) {7}, {8}, {9}\n"\
"\n"\
"**{10} fastest lap:** []({11}) {12}, {13}, {14}\n"\
"\n"\
"**{15} winner:** []({16}) {17}, {18}\n"\
"\n"

hub_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"| Session | UTC | Weather forecast|\n"\
"| - | - | - |\n| Free Practice 1 | {3} | []({4}) {5}, {6} °C / {7} °F|\n"\
"| Free Practice 2 | {8} | []({9}) {10}, {11} °C / {12} °F|\n"\
"| Free Practice 3 | {13} | []({14}) {15}, {16} °C / {17} °F|\n"\
"| Qualifying | {18} | []({19}) {20}, {21} °C / {22} °F|\n"\
"| Race | {23} | []({24}) {25}, {26} °C / {27} °F|\n"\
"\n"\
"[Click here](http://f1calendar.com/) for start times in your area.\n"\
"\n"\
"Please note that this weather forecast does not get updated. For an up-to-date weather forecast, see the sidebar.\n"\
"\n"\
"---\n"\
"\n"\
"Hi there, r/formula1!\n"\
"\n"\
"Having fun in person at the {28} {29} Grand Prix?\n"\
"\n"\
"These posts will be a useful resource for anyone looking for feedback on the event when planning to attend in future so please feel free to leave detailed feedback and information!\n"\
"\n"\
"Please use this post for all the below:\n"\
"\n"\
"- Let us know how you are enjoying the atmosphere at the event in person! Post your thoughts and comments here.\n"\
"- Use this post to arrange any impromptu meet-ups at the GP, if you’d like.\n"\
"- Use Imgur or other image hosting websites to share pictures of\n"\
" - Your view from the grandstand\n"\
" - Yourself at the grandstand\n"\
" - Driver’s parade\n"\
" - Funny shaped clouds creating rain hype\n"\
" - Other generic pictures from the event\n"\
"- Provide detailed feedback about the event as an attendee\n"\
"\n"\
"**Please note:** Standalone posts of these topics outside these threads will NOT be allowed, and will be removed in all cases (a few exceptional and very unique posts may be allowed based on moderator discretion).\n"\
"\n"\
"Resources:\n"\
"\n"\
"- The subreddit [Circuit Guide](/r/formula1/wiki/circuitguide). Users can edit and update the wiki for the benefit of the community so please feel free to do so!"

old_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {11} |\n"\
"| Free Practice 2 | {12} |\n"\
"| Free Practice 3 | {13} |\n"\
"| Qualifying | {14} |\n"\
"| Race | {15} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {16}\n"\
"\n"\
"**Length:** {17} km ({18:.3f} mi)\n"\
"\n"\
"**Distance:** {19} laps, {20} km ({21:.3f} mi)\n"\
"\n"\
"{22}{23}---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({24}.html)\n"\
"- Wiki: [Race]({25}) | [{26}]({27})\n"\
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
"Remember to update your F1 Fantasy team. Join the [official subreddit league here](https://fantasy.formula1.com/join/?=7d693ab9b8), or use invite code `7d693ab9b8`."

new_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {11} |\n"\
"| Free Practice 2 | {12} |\n"\
"| Free Practice 3 | {13} |\n"\
"| Qualifying | {14} |\n"\
"| Race | {15} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {16}\n"\
"\n"\
"**Length:** {17} km ({18:.3f} mi)\n"\
"\n"\
"**Distance:** {19} laps, {20} km ({21:.3f} mi)\n"\
"\n"\
"{22}{23}---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({24}.html)\n"\
"- Wiki: [Race]({25}) | [{26}]({27})\n"\
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
"Remember to update your F1 Fantasy team. Join the [official subreddit league here](https://fantasy.formula1.com/join/?=7d693ab9b8), or use invite code `7d693ab9b8`."

post_session_template = "### ROUND {0}: {1} []({2})\n"\
"\n"\
"|{3}|\n"\
"|:-:|\n"\
"|{4} {5} {6} - {7} {8} {9}|\n"\
"|{10}|\n"\
"\n"\
"| Session | UTC |\n"\
"| - | - |\n"\
"| Free Practice 1 | {11} |\n"\
"| Free Practice 2 | {12} |\n"\
"| Free Practice 3 | {13} |\n"\
"| Qualifying | {14} |\n"\
"| Race | {15} |\n"\
"\n"\
"[Click here for start times in your area.](http://f1calendar.com/)\n"\
"\n"\
"---\n"\
"\n"\
"#### {16}\n"\
"\n"\
"**Length:** {17} km ({18:.3f} mi)\n"\
"\n"\
"**Distance:** {19} laps, {20} km ({21:.3f} mi)\n"\
"\n"\
"{22}[](/resultsBegin)[](/resultsEnd)\n"\
"\n"\
"---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- F1.com: [Race]({23}.html)\n"\
"- Wiki: [Race]({24}) | [{25}]({26})\n"\
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

testing_template = "|{0}|\n"\
"|:-:|\n"\
"|{1} - {2}|\n"\
"|{3}|\n"\
"\n"\
"---\n"\
"\n"\
"#### {4}\n"\
"\n"\
"**Length:** {5} km ({6:.3f} mi)\n"\
"\n"\
"**Lap record:** []({7}) {8}, {9}, {10}, {11}\n"\
"\n"\
"**{12} pole:** []({13}) {14}, {15}, {16}\n"\
"\n"\
"**{17} fastest lap:** []({18}) {19}, {20}, {21}\n"\
"\n"\
"---\n"\
"\n"\
"####Useful links\n"\
"\n"\
"- Wiki: [{22}]({23})\n"\
"\n"\
"---\n"\
"\n"\
"#### Streaming & Downloads\n"\
"\n"\
"For information on streams, please visit /r/MotorSportsStreams. Please do not post information about streams in this thread. Thank you.\n"\
"\n"\
"---\n"\
"\n"\
"#### Discussion\n"\
"\n"\
"Join us on /r/formula1's IRC chat: **[#f1 on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1/)**\n"\
"\n"\
"Stream talk has a channel of it's own: **[#f1streams on irc.snoonet.org](https://kiwiirc.com/client/irc.snoonet.org/f1streams)**\n"\
"\n"\
"Be sure to check out the **[Discord](https://discordapp.com/invite/WcJsaqf)** as well.\n"
