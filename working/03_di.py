import webbrowser

import discogs_client
import pandas as pd
import os
import re
import numpy as np

os.chdir('C:\\Users\\todd9\\OneDrive\\Projects\\py_RecColl')
# coll = pd.read_csv('coll.csv')
token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
lp = []


# Isolate release ID from csv and query for details
coll = pd.read_csv('coll.csv')
lp = coll[coll['Format'].str.contains('LP')]
randlp = lp.sample(1)
print("randlp...")
print(randlp)

randomartist = randlp['Artist']
randomartist = re.sub("[(][0-9][0-9][)]", "", randomartist.to_string(index=False))
randomartist = re.sub("[(][0-9][)]", "", randomartist)
randomalbum = randlp['Title']
randomsel = randomartist + ' - ' + randomalbum
print(randomsel)

randid = randlp['release_id'].values
randid = np.array2string(randid[0])
# apidata = d.release(1355714).artists[0].name
# print(apidata)
apiartist = d.release(randid).artists[0].name
apiartist = re.sub("[(][0-9][0-9][)]", "", apiartist)
apiartist = re.sub("[(][0-9][)]", "", apiartist)
apialbum = d.release(randid).title
ast = '*'
if len(apiartist) > len(apialbum):
    print(ast.rjust(len(apiartist), ast) + "\n" + apiartist + "\n" + apialbum + "\n" + ast.rjust(len(apiartist), ast))
else:
    print(ast.rjust(len(apialbum), ast) + "\n" + apiartist + "\n" + apialbum + "\n" + ast.rjust(len(apialbum), ast))



