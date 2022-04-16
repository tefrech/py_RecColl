# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020
@author: todd9
"""
import discogs_client
import pandas as pd
import re
from flask import Flask, render_template, request
# import os
import time
import random

# Test mode 0 = No, 1 = Yes
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
    print("Importing from CSV...")
    # PULLING FROM CSV FOR TESTING
    # filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl\\static'
    # os.chdir(filedir)
    coll = pd.read_csv('static/coll.csv')
    # Pull just the release_id column for each format; extract the values to lists
    coll12 = coll['release_id'][coll['Format'].str.contains('12')].values.tolist()
    coll7 = coll['release_id'][coll['Format'].str.contains('7')].values.tolist()
    coll10 = coll['release_id'][coll['Format'].str.contains('10')].values.tolist()
    # filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl'
    # os.chdir(filedir)
else:
    # Start downloading collection
    print("Pulling collection from Discogs...")
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
    index12 = folderdf.index[folderdf.fname == 'LP - 12"'].tolist()[0]
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
    # Count releases
    lenfull7 = len(full7)
    print("7"":", lenfull7)
    rl7 = range(0, lenfull7)
    # Make a blank list
    coll7 = []
    # Iterate the Release IDs into their own list with the int type
    for i in rl7:
        coll7.append(full7[i].id)
    # LP
    discogs12 = me.collection_folders[index12].releases
    full12 = []
    range12 = range(0, discogs12.pages)
    for x in range12:
        full12 = full12 + discogs12.page(x)
    # Count releases
    lenfull12 = len(full12)
    print("LP/12"":", lenfull12)
    rl12 = range(0, lenfull12)
    # Make a blank list
    coll12 = []
    # Iterate the Release IDs into their own list with the int type
    for i in rl12:
        coll12.append(full12[i].id)
    # 10"
    discogs10 = me.collection_folders[index10].releases
    full10 = []
    range10 = range(0, discogs10.pages)
    for x in range10:
        full10 = full10 + discogs10.page(x)
    # Count releases
    lenfull10 = len(full10)
    print("10"":", lenfull10)
    rl10 = range(0, lenfull10)
    # Make a blank list
    coll10 = []
    # Iterate the Release IDs into their own list with the int type
    for i in rl10:
        coll10.append(full10[i].id)

# Start app
app = Flask(__name__, template_folder='templates')


# Start at index.html
@app.route('/', methods=['GET', 'POST', 'GET/POST'])
def index():
    return render_template('index.html')


# Spin
@app.route('/spin', methods=['GET', 'POST', 'GET/POST'])
def spin():
    if request.form['format'] == 'lp':
        # Pick a random release from the list
        random_id = random.choice(coll12)
        # random_id = coll12[['release_id']].sample(1).values.__int__()
        format_desc = 'LP/12"'
    elif request.form['format'] == 's':
        # Pick a random release from the list
        random_id = random.choice(coll7)
        # random_id = coll7[['release_id']].sample(1).values.__int__()
        format_desc = '7"'
    else:
        # Pick a random release from the list
        random_id = random.choice(coll10)
        # random_id = coll10[['release_id']].sample(1).values.__int__()
        format_desc = '10"'
    random_release = d.release(random_id)
    random_artist = random_release.artists
    print(random_artist[0].name)
    # Pull artist and remove extra (#)
    # artist = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", random_artist[0].name))
    if len(random_release.artists) > 1:
        random_artists = random_release.artists
        artist_count = len(random_release.artists)
        artist_count_range = range(0, artist_count)
        artist_names = []
        for r in artist_count_range:
            artist_names.append(re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", random_artists[r].name)))
        artist_names = ' & '.join(artist_names)
    else:
        # artist_count = len(random_release.artists)
        artist_names = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", random_release.artists[0].name))
    # Pull release title
    album = random_release.title
    # Combo in string
    t = artist_names + ' - ' + album
    print(t)
    try:
        cover = random_release.images[0]['uri']
    except(KeyError, TypeError, AttributeError):
        try:
            cover = random_release.master.images[0]['uri']
        except(KeyError, TypeError, AttributeError) as e:
            print(e, 'url error')
            cover = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
    try:
        cover_width = random_release.images[0]['width']
        if cover_width >= 500:
            cover_width = 500
        elif cover_width < 500:
            cover_width = random_release.master.images[0]['width']
            if cover_width >= 500:
                cover_width = 500
            else:
                cover_width = random_release.master.images[0]['width']
        else:
            cover_width = random_release.images[0]['width']
    except(KeyError, TypeError, AttributeError) as e:
        print(e, 'width error')
        try:
            cover_width = random_release.master.images[0]['width']
            if cover_width >= 500:
                cover_width = 500
            else:
                cover_width = random_release.master.images[0]['width']
        except(KeyError, TypeError, AttributeError) as e:
            print(e, 'width = 200')
            cover_width = 200
    print(cover)
    rformat = random_release.formats
    # Try block to get vinyl color, otherwise it returns "Black"
    try:
        color = rformat[0]['text']
    except KeyError:
        color = 'Black'
    time.sleep(1)
    while True:
        try:
            return render_template('spin.html', riwidth=cover_width, t=t, rartist=artist_names, ralbum=album,
                                   formatcolor=color, rimageurl=cover, formatdesc=format_desc)
        except (UnicodeError, UnicodeDecodeError) as e:
            return "Trying again..."


if __name__ == '__main__':
    app.run(debug=True)
