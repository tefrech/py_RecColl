# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020

@author: todd9
"""
import discogs_client
# import os
import pandas as pd
import re
import dominate
import numpy as np
from dominate.tags import *
from flask import Flask, render_template

# Initial loading of collections via API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
folders = me.collection_folders
l = len(folders)
# Setup empty variables
folids = []
fnames = []
# Pull elements into lists
for i in range(l):
    folids.append(folders[i].id)
    fnames.append(folders[i].name)
# Write lists to a dataframe
fdf = pd.DataFrame({'fid': folids, 'fname': fnames})

# 7"s
seven = me.collection_folders[4].releases
sevfulllist = []
sevmaxpage = seven.pages
sevprange = range(0, sevmaxpage)
for x in sevprange:
    sevfulllist = sevfulllist+seven.page(x)
sevfulllist = pd.DataFrame(sevfulllist)

# 10"s
tenin = me.collection_folders[1].releases
tenfulllist = []
tenmaxpage = tenin.pages
tenprange = range(0, tenmaxpage)
for x in tenprange:
    tenfulllist = tenfulllist+tenin.page(x)
tenfulllist = pd.DataFrame(tenfulllist)

# lps
lp = me.collection_folders[7].releases
fulllistlp = []
maxpagelp = lp.pages
prangelp = range(0, maxpagelp)
for x in prangelp:
    fulllistlp = fulllistlp+lp.page(x)
fulllistlp = pd.DataFrame(fulllistlp)



app = Flask(__name__, template_folder='temp_test')


## It won't open the html files in the correct location, need to figure out file structure


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/lpspin', methods=['POST'])
def lpspin():
    # Pulling a random entry, release_id
    ra = fulllistlp.sample(1)
    ra = np.array2string(ra[0].values)
    ra = ra.split(' ')
    ra = ra[1]
    release = d.release(ra)
    rartist = release.artists[0].name
    rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
    rartist = re.sub("[(][0-9][)]", "", rartist)
    ralbum = release.title
    rimageurl = release.images[0]['uri']
    if release.images[0]['width'] > 500:
        rimgwid = release.images[0]['width'] * 0.6
    else:
        rimgwid = release.images[0]['width']
    if release.images[0]['height'] > 500:
        rimghei = release.images[0]['height'] * 0.6
    else:
        rimghei = release.images[0]['height']
    t = rartist + ' - ' + ralbum
    print(t)
    doc = dominate.document(title=t)
    with doc.head:

        link(rel="preconnect", href="https://fonts.googleapis.com")
        link(rel="preconnect", href="https://fonts.gstatic.com")
        link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Roboto+Serif:wght"
                                    "@100&family=Roboto+Slab:wght@500&display=swap")
        script(src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js")
        script(src="static/js.js", type="text/javascript")
        link(rel="stylesheet", href="static/style.css")
    with doc:
        with div(cls='title', align='center'):
            h1(rartist.upper())
            h2(ralbum.upper())
            with div(id='img'):
                img(src=rimageurl, width=rimgwid, height=rimghei)
        with div(id='button', align='center'):
            with form(action="/lpspin", method="post", cls="spin"):
                button("LP SPIN!", name="forwardBtn", type="submit")
            with form(action="/sevspin", method="post", cls="spin"):
                button("SEVEN INCH SPIN!", name="forwardBtn7", type="submit")
            with form(action="/tenspin", method="post", cls="spin"):
                button("TEN IN SPIN!", name="forwardBtn10", type="submit")
    docstr = str(doc)
    f = open('lpspin.html', 'w')
    f.write(docstr)
    f.close()
    # print(t)
    # return render_template('lpspin.html')
    return docstr


@app.route('/sevspin', methods=['POST'])
def sevspin():
    # Pulling a random entry, release_id
    ra = sevfulllist.sample(1)
    ra = np.array2string(ra[0].values)
    ra = ra.split(' ')
    ra = ra[1]
    release = d.release(ra)
    rartist = release.artists[0].name
    rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
    rartist = re.sub("[(][0-9][)]", "", rartist)
    ralbum = release.title
    rimageurl = release.images[0]['uri']
    t = rartist + ' - ' + ralbum
    print(t)
    doc = dominate.document(title=t)
    with doc.head:
        link(rel='stylesheet', href='static/style.css')
        link(rel="preconnect", href="https://fonts.googleapis.com")
        link(rel="preconnect", href="https://fonts.gstatic.com")
        link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Roboto+Serif:wght"
                                    "@100&family=Roboto+Slab:wght@500&display=swap")
        script(src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js")
        script(src="static/js.js", type="text/javascript")
        link(rel="stylesheet", href="static/style.css")
    with doc:
        with div(cls='title', align='center'):
            h1(rartist.upper())
            h2(ralbum.upper())
            with div(id='img'):
                img(src=rimageurl)
        with div(id='button', align='center'):
            with form(action="/lpspin", method="post", cls="spin"):
                button("LP SPIN!", name="forwardBtn", type="submit")
            with form(action="/sevspin", method="post", cls="spin"):
                button("SEVEN INCH SPIN!", name="forwardBtn7", type="submit")
            with form(action="/tenspin", method="post", cls="spin"):
                button("TEN IN SPIN!", name="forwardBtn10", type="submit")
    docstr = str(doc)
    f = open('sevspin.html', 'w')
    f.write(docstr)
    f.close()
    # print(t)
    # return render_template('sevspin.html')
    return docstr


@app.route('/tenspin', methods=['POST'])
def tenspin():
    # Pulling a random entry, release_id
    ra = tenfulllist.sample(1)
    ra = np.array2string(ra[0].values)
    ra = ra.split(' ')
    ra = ra[1]
    release = d.release(ra)
    rartist = release.artists[0].name
    rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
    rartist = re.sub("[(][0-9][)]", "", rartist)
    ralbum = release.title
    rimageurl = release.images[0]['uri']
    t = rartist + ' - ' + ralbum
    print(t)
    doc = dominate.document(title=t)
    with doc.head:
        link(rel='stylesheet', href='static/style.css')
        link(rel="preconnect", href="https://fonts.googleapis.com")
        link(rel="preconnect", href="https://fonts.gstatic.com")
        link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Roboto+Serif:wght"
                                    "@100&family=Roboto+Slab:wght@500&display=swap")
        script(src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js")
        script(src="static/js.js", type="text/javascript")
        link(rel="stylesheet", href="static/style.css")
    with doc:
        with div(cls='title', align='center'):
            h1(rartist.upper())
            h2(ralbum.upper())
            with div(id='img'):
                img(src=rimageurl)
        with div(id='button', align='center'):
            with form(action="/lpspin", method="post", cls="spin"):
                button("LP SPIN!", name="forwardBtn", type="submit")
            with form(action="/sevspin", method="post", cls="spin"):
                button("SEVEN INCH SPIN!", name="forwardBtn7", type="submit")
            with form(action="/tenspin", method="post", cls="spin"):
                button("TEN IN SPIN!", name="forwardBtn10", type="submit")
    docstr = str(doc)
    f = open('tenspin.html', 'w')
    f.write(docstr)
    f.close()
    # print(t)
    return docstr





if __name__ == '__main__':
    app.run(debug=True)
