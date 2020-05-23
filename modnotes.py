#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This code was written for /r/formula1
Written by /u/BottasWMR and /u/Redbiertje
23 May 2020
"""


#Imports
import sys
import os
import numpy as np
import json
import base64
import zlib
import time
from psaw import PushshiftAPI


def get_b64_usernotes(r):
    """
    Pulls the /r/Formula1/wiki/usernotes page and returns the base-64 blob container usernotes
    """
    raw_page = r.subreddit('formula1').wiki['usernotes'].content_md
    decoded_page = json.JSONDecoder().decode(raw_page)
    return decoded_page['blob']

def decode_usernotes(b64_blob):
    """
    Decodes the base-64 usernote blob into a JSON object and then returns it as a Python-editable object
    """
    binary = base64.standard_b64decode(b64_blob)
    json_formatted = zlib.decompress(binary)
    json_formatted = json_formatted.decode('utf8')
    return json.JSONDecoder().decode(json_formatted)

def add_dd_count(r, userdict):
    """
    Input a dictionary with a key of users and contents DD removals for each user
    Returns the edited notes file
    """
    notes = decode_usernotes(get_b64_usernotes(r))
    for user in userdict:
        sum_to_add = userdict[user]
        if user in notes:
            DDR_changed = 0
            for note in notes[user]['ns']:
                if 'DDR count' in note['n']:
                    count = int(note['n'][12:])
                    notes[user]['ns'].remove(note)
                    notes[user]['ns'].insert(0,{'n': f'DDR count - ' + str(count + sum_to_add), 't': int(time.time()),'m': 12, 'w': 10})
                    DDR_changed = 1
                if DDR_changed == 0:
                    notes[user]['ns'].insert(0,{'n': f'DDR count - ' + str(sum_to_add), 't': str(int(time.time())), 'm': 12, 'w': 10})
                    DDR_changed = 1
        else:
            notes[user] = {'ns': [{'n': 'DDR count - ' + str(sum_to_add), 't': str(int(time.time())), 'm': 12, 'w': 10}]}
    return notes

def encode_usernotes(notes):
    """
    Encodes edited usernotes into base-64 blob and returns that blob
    """
    json_notes = json.JSONEncoder().encode(notes)
    json_notes = json_notes.encode()
    binary = zlib.compress(json_notes)
    return base64.standard_b64encode(binary)

def upload_usernotes(r, b64_blob):
    """
    Uploads the blob onto /r/formula1/wiki/usernotes
    """
    raw_page = r.subreddit('formula1').wiki['usernotes'].content_md
    decoded_page = json.JSONDecoder().decode(raw_page)
    decoded_page['blob'] = b64_blob.decode('utf8')
    encoded_page = json.JSONEncoder().encode(decoded_page)
    r.subreddit('Formula1').wiki['usernotes'].edit(encoded_page)

def find_DD_removals(r):
    """
    Finds DD removal comments in past 24 hours and gets the author of the original post, returns dictionary of authors and frequency
    Offset 10,000 seconds to account for delay in comments being indexed by pushshift
    """
    api = PushshiftAPI(r)
    DDRs = {}
    authors = []
    removals = list(api.search_comments(after=int(time.time()) - 96400,
                                before=int(time.time())-10000,
                                subreddit='formula1',
                                q='This post has been removed. It should be posted in one of the stickied threads or the Daily Discussion instead.',
                                limit=499))
    for c in removals:
        #s = praw.models.Submission(r, c.link_id[3:])
        s = r.submission(id=c.link_id[3:])
        if s.author != None:
            if s.author.name in DDRs:
                DDRs[s.author.name] += 1
            else:
                DDRs[s.author.name] = 1
    return DDRs

def update_modnotes_DD(r):
    """
    Executes the procedure for updating the usernotes for DD removals
    """
    try:
        upload_usernotes(r, encode_usernotes(add_dd_count(r, find_DD_removals(r))))
        return True
    except Exception as e:
        print("Error in modnotes.update_usernotes_DD: {}".format(e))
        return False