# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020
@author: todd9
"""
# import block
import discogs_client
import pandas as pd
import re
import time
# import dominate
# import numpy as np
# from dominate.tags import *
# from dominate.util import raw
from flask import Flask, render_template, request
import os
from celery import Celery

# PULLING FROM CSV FOR TESTING
filedir = ('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl\\static')
os.chdir(filedir)
coll = pd.read_csv('coll.csv')
lpspinc = coll[coll['Format'].str.contains('LP')]
sevspinc = coll[coll['Format'].str.contains('7')]
tenspinc = coll[coll['Format'].str.contains('10')]
filedir = ('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl')
os.chdir(filedir)

# Start app
app = Flask(__name__, template_folder='temp_test')
# app = Flask(__name__, template_folder='templates')

# Initial loading of collections via API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
folders = me.collection_folders
leng = len(folders)
r = range(0, leng)
# TODO: Pull in folders and isolate Folder ID for each format
# # Setup empty variables
# folids = []
# fnames = []
# # Pull elements into lists
# for i in range(leng):
#     folids.append(folders[i].id)
#     fnames.append(folders[i].name)
# # Write lists to a dataframe
# fdf = pd.DataFrame({'fid': folids, 'fname': fnames})

# Create LP collection
# lp = me.collection_folders[7].releases
# fulllistlp = []
# maxpagelp = lp.pages
# prangelp = range(0, maxpagelp)
# for x in prangelp:
#     fulllistlp = fulllistlp + lp.page(x)
# lpspinc = pd.DataFrame(fulllistlp)

# Create 7" collection
# seven = me.collection_folders[4].releases
# sevfulllist = []
# sevmaxpage = seven.pages
# sevprange = range(0, sevmaxpage)
# for x in sevprange:
#     sevfulllist = sevfulllist + seven.page(x)
# sevenspinc = pd.DataFrame(sevfulllist)

# Create 10" collection
# tenin = me.collection_folders[1].releases
# tenfulllist = []
# tenmaxpage = tenin.pages
# tenprange = range(0, tenmaxpage)
# for x in tenprange:
#     tenfulllist = tenfulllist + tenin.page(x)
# tenspinc = pd.DataFrame(tenfulllist)

riwidth = []
t = []
rartist = []
ralbum = []
formatcolor = []
rimageurl = []
formatdesc = []

# Start at index.html
@app.route('/', methods=['GET', 'POST', 'GET/POST'])
def index():
    return render_template('index.html')


# Spin
@app.route('/spin', methods=['GET', 'POST', 'GET/POST'])
def spin():
    if request.form['format'] == 'lp':
        rel = lpspinc.sample(1)
    elif request.form['format'] == 's':
        rel = sevspinc.sample(1)
    else:
        rel = tenspinc.sample(1)
    rel = d.release(rel[['release_id']].values.__int__())
    rartist = rel.artists[0].name
    rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
    rartist = re.sub("[(][0-9][)]", "", rartist)
    ralbum = rel.title
    t = rartist + ' - ' + ralbum
    try:
        rimageurl = rel.images[0]['uri']
        if (rel.images[0]['width'] > 500):
            riwidth = 500
        else:
            riwidth = rel.images[0]['width']
    except (KeyError, TypeError, AttributeError):
        rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
        riwidth = 1
    rformat = rel.formats
    # Try block to get vinyl color, otherwise it returns "Black"
    try:
        formatcolor = rformat[0]['text']
    except KeyError:
        formatcolor = 'Black'
    try:
        formatdesc = rformat[0]['descriptions'][0]
    except KeyError:
        formatdesc = 'LP'
    while True:
        try:
            return render_template('spin.html', riwidth=riwidth, t=t, rartist=rartist, ralbum=ralbum,
                                   formatcolor=formatcolor, rimageurl=rimageurl, formatdesc=formatdesc)
        except (UnicodeError, UnicodeDecodeError) as e:
            return "Trying again..."

#
# # LP Spin
# @app.route('/lpspin', methods=['GET', 'POST', 'GET/POST'])
# def lpspin():
#     rel = lpspinc.sample(1)
#     rel = d.release(rel[['release_id']].values.__int__())
#     rartist = rel.artists[0].name
#     rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
#     rartist = re.sub("[(][0-9][)]", "", rartist)
#     rartist = rartist.upper()
#     ralbum = rel.title
#     ralbum = ralbum.upper()
#     t = rartist + ' - ' + ralbum
#     try:
#         rimageurl = rel.images[0]['uri']
#     except (KeyError, TypeError, AttributeError):
#         rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
#     if rel.images[0]['width'] > 600:
#         riwidth = 600
#     else:
#         riwidth = rel.images[0]['width']
#     rformat = rel.formats
#     # Try block to get vinyl color, otherwise it returns "Black"
#     try:
#         formatcolor = rformat[0]['text']
#     except KeyError:
#         formatcolor = 'Black'
#     formatcolor = formatcolor.upper()
#     try:
#         formatdesc = rformat[0]['descriptions'][0]
#     except KeyError:
#         formatdesc = 'LP'
#     while True:
#         try:
#             return render_template('spin.html', riwidth=riwidth, t=t, rartist=rartist, ralbum=ralbum,
#                                    formatcolor=formatcolor, rimageurl=rimageurl, formatdesc=formatdesc)
#         except (UnicodeError, UnicodeDecodeError) as e:
#             return "Trying again..."
#
#
# # Seven inch spin
# @app.route('/sevspin', methods=['GET', 'POST', 'GET/POST'])
# def sevspin():
#     # Pulling a random entry
#     rel = sevspinc.sample(1)
#     rel = d.release(rel[['release_id']].values.__int__())
#     rartist = rel.artists[0].name
#     rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
#     rartist = re.sub("[(][0-9][)]", "", rartist)
#     rartist = rartist.upper()
#     ralbum = rel.title
#     ralbum = ralbum.upper()
#     t = rartist + ' - ' + ralbum
#     try:
#         rimageurl = rel.images[0]['uri']
#     except (KeyError, TypeError, AttributeError):
#         rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
#     if rel.images[0]['width'] > 600:
#         riwidth = 600
#     else:
#         riwidth = rel.images[0]['width']
#     if rel.images[0]['height'] > 500:
#         riheight = rel.images[0]['height'] * 0.6
#     else:
#         riheight = rel.images[0]['height']
#     rformat = rel.formats
#     # Try block to get vinyl color, otherwise it returns "Black"
#     try:
#         formatcolor = rformat[0]['text']
#     except KeyError:
#         formatcolor = 'Black'
#     try:
#         formatdesc = rformat[0]['descriptions'][0]
#     except KeyError:
#         formatdesc = 'LP'
#     formatcolor = formatcolor.upper()
#     while True:
#         try:
#             return render_template('spin.html', formatdesc=formatdesc, riwidth=riwidth, t=t, rartist=rartist,
#                                    ralbum=ralbum, formatcolor=formatcolor, rimageurl=rimageurl, rformat=rformat)
#         except (UnicodeError, UnicodeDecodeError) as e:
#             return "Trying again..."
#
#
# # Ten inch spin
# @app.route('/tenspin', methods=['GET', 'POST', 'GET/POST'])
# def tenspin():
#     # Pulling a random entry
#     rel = tenspinc.sample(1)
#     rel = d.release(rel[['release_id']].values.__int__())
#     rartist = rel.artists[0].name
#     rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
#     rartist = re.sub("[(][0-9][)]", "", rartist)
#     rartist = rartist.upper()
#     ralbum = rel.title
#     ralbum = ralbum.upper()
#     t = rartist + ' - ' + ralbum
#     try:
#         rimageurl = rel.images[0]['uri']
#     except KeyError:
#         rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
#     if rel.images[0]['width'] > 600:
#         riwidth = 600
#     else:
#         riwidth = rel.images[0]['width']
#     if rel.images[0]['height'] > 500:
#         riheight = rel.images[0]['height'] * 0.6
#     else:
#         riheight = rel.images[0]['height']
#     rformat = rel.formats
#     # Try block to get vinyl color, otherwise it returns "Black"
#     try:
#         formatcolor = rformat[0]['text']
#     except KeyError:
#         formatcolor = 'Black'
#     try:
#         formatdesc = rformat[0]['descriptions'][0].upper()
#     except KeyError:
#         formatdesc = 'LP'
#     formatcolor = formatcolor.upper()
#     while True:
#         try:
#             return render_template('spin.html', riwidth=riwidth, riheight=riheight, t=t, rartist=rartist,
#                                    ralbum=ralbum, formatcolor=formatcolor, rimageurl=rimageurl, formatdesc=formatdesc)
#         except (UnicodeError, UnicodeDecodeError) as e:
#             return "Trying again..."
#

if __name__ == '__main__':
    app.run(debug=True)