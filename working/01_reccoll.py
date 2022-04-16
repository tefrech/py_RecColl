# -*- coding: utf-8 -*-
"""
Created on Sat Nov 28 23:13:41 2020

@author: todd9
"""
import sys
import discogs_client
import os
import pandas as pd
import re
import requests
import json
import time
import webbrowser
import dominate
from dominate.tags import *
from faker import Factory

os.chdir('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl')
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
coll = pd.read_csv('coll.csv')
lp = coll[coll['Format'].str.contains('LP')]
# Force it to return an Artist with (#) to confirm the regex is working and skip waiting
# lp = lp[lp['Artist'].str.contains('[(][0-9][)]')]
randomlp = lp.sample(1)
randomartist = randomlp['Artist']
randomartist = re.sub("[(][0-9][0-9][)]", "", randomartist.to_string(index=False))
randomartist = re.sub("[(][0-9][)]", "", randomartist)
randomalbum = randomlp['Title']
randomalbum = randomalbum.to_string(index=False)
t = randomartist+' - '+randomalbum
print(t)

res = d.search(release_title=randomalbum, artist=randomartist, type='release')
mid = res.page(1)[0].id
midim = d.release(mid).images
midm = d.release(mid).master.images[0]['uri']

fake = Factory.create()
doc = dominate.document(title=randomartist+' - '+randomalbum)

with doc.head:
    link(rel='stylesheet', href='01_style.css')

with doc:
    body(style='background-color:'+fake.hex_color()+'; color:'+fake.hex_color())
    with div(id='title', align='center'):
        h1(randomartist)
        h2(randomalbum)
        with div(id='img'):
            a(img(src=midm), href=midm)

docstr = str(doc)

f = open('i.html', 'w')
f.write(docstr)
f.close()
print(doc)
# webbrowser.open('i.html')


