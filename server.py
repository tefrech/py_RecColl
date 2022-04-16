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

# Initial loading of collections via API
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
folders = me.collection_folders
leng = len(folders)
r = range(0, leng)
riwidth = ['']
t = []
rartist = []
ralbum = []
formatcolor = []
rimageurl = []
formatdesc = []

# # # Setup empty variables
# folids = []
# fnames = []
# # Pull elements into lists
# for i in range(leng):
#     folids.append(folders[i].id)
#     fnames.append(folders[i].name)
# # Write lists to a dataframe
# fdf = pd.DataFrame({'fid': folids, 'fname': fnames})
# tenid = fdf['fid'][fdf.fname == '10"']
# sevenid = fdf['fid'][fdf.fname == '7"']
# lpid = fdf['fid'][fdf.fname == 'LP - Audited']

# Create LP collection
lp = me.collection_folders[7].releases
fulllistlp = []
maxpagelp = lp.pages
prangelp = range(0, maxpagelp)
for x in prangelp:
    fulllistlp = fulllistlp + lp.page(x)
lpspinc = pd.DataFrame(fulllistlp)
# Create 7" collection
seven = me.collection_folders[4].releases
sevfulllist = []
sevmaxpage = seven.pages
sevprange = range(0, sevmaxpage)
for x in sevprange:
    sevfulllist = sevfulllist + seven.page(x)
sevenspinc = pd.DataFrame(sevfulllist)
# Create 10" collection
tenin = me.collection_folders[1].releases
tenfulllist = []
tenmaxpage = tenin.pages
tenprange = range(0, tenmaxpage)
for x in tenprange:
    tenfulllist = tenfulllist + tenin.page(x)
tenspinc = pd.DataFrame(tenfulllist)


# Start at index.html
@app.route('/', methods=['GET', 'POST', 'GET/POST'])
def index():
    return render_template('index.html')


# Spin
@app.route('/spin', methods=['GET', 'POST', 'GET/POST'])
def spin():
    if request.form['format'] == 'lp':
        rel = lpspinc.sample(1)
        formatdesc = 'LP'
    elif request.form['format'] == 's':
        rel = sevspinc.sample(1)
        formatdesc = '7"'
    else:
        rel = tenspinc.sample(1)
        formatdesc = '10"'
    rel = d.release(rel[['release_id']].values.__int__())
    # Clean up the artist name, removing (2), etc.
    rartist = re.sub("[(][0-9][)]", "", re.sub("[(][0-9][0-9][)]", "", rel.artists[0].name))
    ralbum = rel.title
    t = rartist + ' - ' + ralbum
    try:
        rimageurl = rel.images[0]['uri']
    except(KeyError, TypeError, AttributeError):
        try:
            rimageurl = rel.master.images[0]['uri']
        except(KeyError, TypeError, AttributeError) as e:
            print(e, 'url error')
            rimageurl = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
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