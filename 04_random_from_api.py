import discogs_client
import pandas as pd
import os
import re
import numpy as np
import dominate
from dominate.tags import *
import webbrowser

token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []
folders = me.collection_folders
r = range(0, len(folders))

foldercount: int = len(folders)
# 7"s
in7 = me.collection_folders[4].releases
# 10"s
in10 = me.collection_folders[1].releases
# cassettes
# cass = me.collection_folders[5].releases
# lps
# lp = me.collection_folders[7].releases

curr = in7


fulllist = []
maxpage = curr.pages
pager = range(0, maxpage)
for x in pager:
    fulllist = fulllist+curr.page(x)
fulllist = pd.DataFrame(fulllist)


# Pulling a random entry, release_id
ra = fulllist.sample(1)
ra = np.array2string(ra[0].values)
ra = ra.split(' ')
ra = ra[1]
release = d.release(ra)
artist = release.artists[0].name
artist = re.sub("[(][0-9][0-9][)]", "", artist)
artist = re.sub("[(][0-9][)]", "", artist)
album = release.title
imageurl = release.images[0]['uri']
t = artist + " " + album

format = release.formats
print(artist)
print(album)
print(format)

# Try block to get vinyl color, otherwise it returns "Black"
try:
    formatcolor = format[0]['text']
    print(formatcolor)
except KeyError:
    formatcolor = 'Black'
    print(formatcolor)

try:
    formatdesc = format[0]['descriptions'][0]
    print(formatdesc)
except KeyError:
    formatdesc = '10\"'


try:
    reimguri = release.images[0]['uri']
    print(reimguri)
except KeyError:
    reimguri = "https://s.discogs.com/2f932bf835c333c1e46ad4c768ac79eb3ebdbd2f/images/discogs-white.png"
    print(reimguri)


# reimguri = reimg[0]['uri']



# print(formatcolor)


# rartist = release.artists[0].name
# rartist = re.sub("[(][0-9][0-9][)]", "", rartist)
# rartist = re.sub("[(][0-9][)]", "", rartist)
# ralbum = release.title
# rimageurl = release.images[0]['uri']
# t = rartist + ' - ' + ralbum
# print(t)


