# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020
@author: todd9
"""
# import block
import discogs_client
import pandas as pd
import re
from flask import Flask, render_template, request
import os
import random

# PULLING FROM CSV FOR TESTING
filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl\\static'
os.chdir(filedir)
coll = pd.read_csv('coll.csv')
lpspinc = coll[coll['Format'].str.contains('12')]
sevspinc = coll[coll['Format'].str.contains('7')]
tenspinc = coll[coll['Format'].str.contains('10')]
filedir = 'C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl'
os.chdir(filedir)

# Start app
app = Flask(__name__, template_folder='temp_test')
# app = Flask(__name__, template_folder='templates')

# Setup empty variables
lp = []
riwidth = []
t = []
rartist = []
ralbum = []
formatcolor = []
rimageurl = []
formatdesc = []
folids = []
fnames = []

# Initial loading of collections via API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
# Get folders
# folders = me.collection_folders
# leng = len(folders)
# # Pull elements into lists
# for i in range(leng):
#     folids.append(folders[i].id)
#     fnames.append(folders[i].name)
# # Write lists to a dataframe
# fdf = pd.DataFrame({'fid': folids, 'fname': fnames})
# # Write index value to a list and select the value
# tenindex = fdf.index[fdf.fname == '10"'].tolist()[0]
# lpindex = fdf.index[fdf.fname == 'LP - Audited'].tolist()[0]
# sevenindex = fdf.index[fdf.fname == '7" - Audited'].tolist()[0]
# TODO Get release ID from API AND CSV to the same variable (rrid)
# TODO Need to be able to switch the source without touching code
# Use index values to get the folder contents
# # 7"
# seven = me.collection_folders[sevenindex].releases
# sevenfulllist = []
# # Find range of pages in list
# sevenpagerange = range(0, seven.pages)
# # Combine pages into one list
# for x in sevenpagerange:
#     sevenfulllist = sevenfulllist + seven.page(x)
#
# # LP
# lp = me.collection_folders[lpindex].releases
# fulllistlp = []
# prangelp = range(0, lp.pages)
# for x in prangelp:
#     fulllistlp = fulllistlp + lp.page(x)
#
# # 10"
# tenin = me.collection_folders[tenindex].releases
# tenfulllist = []
# tenprange = range(0, tenin.pages)
# for x in tenprange:
#     tenfulllist = tenfulllist + tenin.page(x)


# Start at index.html
@app.route('/', methods=['GET', 'POST', 'GET/POST'])
def index():
    return render_template('index.html')


# Spin
@app.route('/spin', methods=['GET', 'POST', 'GET/POST'])
def spin():

    if request.form['format'] == 'lp':
        # Pick a random release from the list
        rr = random.choice(sevenfulllist)
        formatdesc = 'LP'
    elif request.form['format'] == 's':
        rel = sevspinc[['release_id']].sample(1).values.__int__()
        formatdesc = '7"'
    else:
        rel = tenspinc[['release_id']].sample(1).values.__int__()
        formatdesc = '10"'
    # rel = d.release(rel[['release_id']].values.__int__())
    # Pull release id from random entry
    # relid = rel.release.id
    # Pull artist and remove extra (#)
    rartist = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", d.release(rel).artists[0].name))
    # Pull release title
    ralbum = d.release(rel).title
    # rel = d.release(2091128)
    # Clean up the artist name, removing (2), etc.
    # rartist = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", rel.artists[0].name))
    # ralbum = rel.title
    t = rartist + ' - ' + ralbum
    try:
        rimageurl = rel.images[0]['uri']
        # riwidth = rel.images[0]['width']
    except(KeyError, TypeError, AttributeError):
        try:
            rimageurl = rel.master.images[0]['uri']
            # riwidth = rel.master.images[0]['width']
        except(KeyError, TypeError, AttributeError) as e:
            print(e, 'url error')
            rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
            # riwidth = 200
    try:
        riwidth = rel.images[0]['width']
        if riwidth >= 500:
            riwidth = 500
        elif riwidth < 500:
                riwidth = rel.master.images[0]['width']
                if riwidth >= 500:
                    riwidth = 500
                else:
                    riwidth = rel.master.images[0]['width']
        else:
            riwidth = rel.images[0]['width']
    except(KeyError, TypeError, AttributeError) as e:
        print(e, 'width error')
        try:
            riwidth = rel.master.images[0]['width']
            if riwidth >= 500:
                riwidth = 500
            else:
                riwidth = rel.master.images[0]['width']
        except(KeyError, TypeError, AttributeError) as e:
            print(e, 'width = 200')
            riwidth = 200
    rformat = rel.formats
    # Try block to get vinyl color, otherwise it returns "Black"
    try:
        formatcolor = rformat[0]['text']
    except KeyError:
        formatcolor = 'Black'
    while True:
        try:
            return render_template('spin.html', riwidth=riwidth, t=t, rartist=rartist, ralbum=ralbum,
                                   formatcolor=formatcolor, rimageurl=rimageurl, formatdesc=formatdesc)
        except (UnicodeError, UnicodeDecodeError) as e:
            return "Trying again..."


if __name__ == '__main__':
    app.run(debug=True)