# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020
@author: todd9
"""
import discogs_client
import pandas as pd
import re
from flask import Flask, render_template, request
import os
import time
import random

# Test mode
testmode = 1

# Setup empty variables
discogs12 = []
riwidth = []
t = []
rartist = []
ralbum = []
formatcolor = []
rimageurl = []
formatdesc = []
folids = []
fnames = []

# Setup Discogs API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()

if testmode == 1:
    # PULLING FROM CSV FOR TESTING
    filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl\\static'
    os.chdir(filedir)
    coll = pd.read_csv('coll.csv')
    coll12 = coll['release_id'][coll['Format'].str.contains('12')].values.tolist()
    coll7 = coll['release_id'][coll['Format'].str.contains('7')].values.tolist()
    coll10 = coll['release_id'][coll['Format'].str.contains('10')].values.tolist()
    filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl'
    os.chdir(filedir)
    randomrelease = d.release(random.choice(coll12))

else:
    # Start downloading collection
    # Get folders
    folders = me.collection_folders
    # Put elements into lists
    flength = len(folders)
    for i in range(flength):
        folids.append(folders[i].id)
        fnames.append(folders[i].name)
    # Write lists to a dataframe
    folderdf = pd.DataFrame({'fid': folids, 'fname': fnames})
    # Write index value to a list and select the value
    index10 = folderdf.index[folderdf.fname == '10"'].tolist()[0]
    index12 = folderdf.index[folderdf.fname == 'LP - Audited'].tolist()[0]
    index7 = folderdf.index[folderdf.fname == '7" - Audited'].tolist()[0]
    # Use index values to get the folder contents
    # 7"
    discogs7 = me.collection_folders[index7].releases
    full7 = []
    # Find range of pages in list
    range7 = range(0, discogs7.pages)
    # Combine pages into one list
    for x in range7:
        full7 = full7 + discogs7.page(x)
    # CONVERT TO LIST OF DISCOGS RELEASE IDS
    # LESS WORK AFTER CLICK
    all7 = []
    lenfull7 = len(full7)
    rl = range(0, lenfull7)
    all7 = []
    for i in rl:
        all7.append(full7[i].id)
    randomrelease = d.release(random.choice(all7))

# randomrelease = d.release(2063284)


# randomchoice = random.choice(full10)
# randomrelease = d.release(randomid)
# randomid = 4874799
# formatdesc = '10"'
# print(randomrelease)
print(randomrelease.artists)

#
if len(randomrelease.artists) > 1:
    randomartists = randomrelease.artists
    artistcount = len(randomrelease.artists)
    artistcountrange = range(0, artistcount)
    artistnames = []
    for r in artistcountrange:
        artistnames.append(re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", randomartists[r].name)))
    artistnames = ' & '.join(artistnames)
else:
    artistcount = len(randomrelease.artists)
    artistnames = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", randomrelease.artists[0].name))

print("Feat:", artistnames)
print(artistcount, " artist(s)")
