# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020

@author: todd9
"""
# import block
import time

import discogs_client
import pandas as pd
import re
import dominate
import numpy as np
from dominate.tags import *
from flask import Flask, render_template, url_for
import os
os.chdir('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl')

# Start app
app = Flask(__name__ , template_folder='temp_test')

# Initial loading of collections via API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
# PULLING FROM CSV FOR TESTING
coll = pd.read_csv('coll.csv')
fulllistlp = coll[coll['Format'].str.contains('LP')]


# folders = me.collection_folders
# leng = len(folders)
# r = range(0, leng)
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


# # Create LP collection
# lp = me.collection_folders[7].releases
# fulllistlp = []
# maxpagelp = lp.pages
# prangelp = range(0, maxpagelp)
# for x in prangelp:
#     fulllistlp = fulllistlp + lp.page(x)
# fulllistlp = pd.DataFrame(fulllistlp)

# # Start at index.html
@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


# LP Spin
@app.route('/lpspin', methods=['GET', 'POST'])
def lpspin(name=None):
    # Pulling a random entry FROM CSV
    rel = fulllistlp.sample(1)
    rel = d.release(rel[['release_id']].values.__int__())
    rartist = rel.artists[0].name
    rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
    rartist = re.sub("[(][0-9][)]", "", rartist)
    ralbum = rel.title
    t = rartist + ' - ' + ralbum
    print(t)
    rimageurl = rel.images[0]['uri']
    if rel.images[0]['width'] > 500:
        rimgwid = rel.images[0]['width'] * 0.6
    else:
        rimgwid = rel.images[0]['width']
    if rel.images[0]['height'] > 500:
        rimghei = rel.images[0]['height'] * 0.6
    else:
        rimghei = rel.images[0]['height']
    rformat = rel.formats
    # print(rformat)
    # Try block to get vinyl color, otherwise it returns "Black"
    try:
        formatcolor = rformat[0]['text']
        # print(formatcolor)
    except KeyError:
        formatcolor = 'Black'
    # print(formatcolor)
    try:
        formatdesc = rformat[0]['descriptions'][0]
        # print(formatdesc)
    except KeyError:
        formatdesc = 'LP'
    try:
        reimguri = rel.images[0]['uri']
        # print(reimguri)
    except KeyError:
        reimguri = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
    # print(reimguri)
    # Return webpage
    css = 'static/style.css'
    doc = dominate.document(title=t)
    with doc.head:
        link(rel="preconnect", href="https://fonts.googleapis.com")
        link(rel="preconnect", href="https://fonts.gstatic.com")
        link(rel="stylesheet", href="https://fonts.googleapis.com/css2?family=Abril+Fatface&family=Roboto+Serif:wght"
                                    "@100&family=Roboto+Slab:wght@500&display=swap")
        script(src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js")
        script(src="static/js.js", type="text/javascript")
        link(rel="stylesheet", href=css, type="text/css")
    with doc:
        with div(cls='title', align='center'):
            h1(rartist.upper())
            h2(ralbum.upper())
            # h3(formatcolor.upper())+" - "+h3(formatdesc.upper())
            with div(id='img'):
                img(src=rimageurl, width=rimgwid, height=rimghei)
        with div(align='center'):
            with form(action="lpspin", method="post", cls="lp"):
                button("LP!", name="forwardBtnlp", type="submit", cls="lp")
            with form(action="sevspin", method="post", cls="s"):
                button("7 INCH!", name="forwardBtn7", type="submit", cls="s")
            with form(action="tenspin", method="post", cls="t"):
                button("10 INCH!", name="forwardBtn10", type="submit", cls="t")
    docstr = str(doc)
    path = 'temp_test/lpspin.html'
    f = open(path, 'w')
    f.write(docstr)
    f.close()
    # print(docstr)
    while True:
        try:
            return render_template('lpspin.html', name=name)
        except (UnicodeError, UnicodeDecodeError) as e:
            return "Trying again..."
        time.sleep(5)



if __name__ == '__main__':
    app.run(debug=True)