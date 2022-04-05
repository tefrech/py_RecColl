import webbrowser

import discogs_client
import pandas as pd
import os
import re
import numpy
import json

os.chdir('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl')
# coll = pd.read_csv('coll.csv')
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []



coll = pd.read_csv('coll.csv')
# ADD A WAY TO EXTRACT FOLDER NAMES, SHOW AS LIST TO CHOOSE FROM
lp = coll[coll['Format'].str.contains('LP')]
randomlp = lp.sample(1)
randomreleaseid = randomlp['release_id']
randomartist = randomlp['Artist']
randomartist = re.sub("[(][0-9][0-9][)]", "", randomartist.to_string(index=False))
randomartist = re.sub("[(][0-9][)]", "", randomartist)
randomalbum = randomlp['Title']
randomalbum = randomalbum.to_string(index=False)
t = randomartist + ' - ' + randomalbum
print(t)

randomreleaseid = randomlp['release_id']
randomreleaseid = randomreleaseid.values
randomreleaseid = numpy.array2string(randomreleaseid)
randomreleaseid = 7112277

print("release id")
print(randomreleaseid)
# print(randomreleaseid.values)
# print(d.release(randomreleaseid).images)


# rid = d.release(randomreleaseid)
releaseidapi = d.search(release_title=randomalbum, artist=randomartist, type='release')
rid = releaseidapi.page(1)[0].id
# rid = 7112277
print("rid / release id")
print(rid)
# ridartist = d.release(rid).artists[0].name
#
# ridimagedata = d.release(rid).images[0]
# print("length / number of images")
# print(len(ridimagedata))
# print("ridimagedata")
# print(json.dumps(ridimagedata))


# ridimagedatauri1 = d.release(rid).images[0]['uri']
# print("ridimagedatauri1")
# print(ridimagedatauri1)
# webbrowser.open(ridimagedatauri1)

# ridimagedatauri1width = d.release(rid).images[0]['width']
# print("ridimagedatauri1width")
# print(ridimagedatauri1width)



# ridimagedataurl2 = [x for x in ridimagedata if x['type'] == 'secondary']
# print("ridimagedatauri2")
# print(ridimagedatauri2)





# for i in me.collection_folders[2].releases
# lp = me.collection_folders[2].releases[0].data['id']
# print(lp.page(1))



# for item in me.collection_folders:
#     # if item.data['name'] == 'LP - 12"':
#
#     print(item.data['name'])
#     print(item.data['id'])
    # print(item.data)
#     fld = item.data['id']
# else: 0
# print(type(item.data))
# ditem = pd.DataFrame(item.data, index=id)

# print(me.collection_folders[4].releases[0])
# print(fld)


# ADD A WAY TO EXTRACT FOLDER NAMES, SHOW AS LIST TO CHOOSE FROM

# Force it to return an Artist with (#) to confirm the regex is working and skip waiting
# lp = lp[lp['Artist'].str.contains('[(][0-9][)]')]

