import discogs_client
import pandas as pd
import numpy as np

token = 'jjxyabmYMHbHDFQvKZJVyYhnlcXTDKEfhmZrHJOm'
d = discogs_client.Client('todd.Frech/0.1', user_token=token)
me = d.identity()
# Pull in list of folders in my collection
folders = me.collection_folders
# Get count of folders
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
# Extract the row for the 7" folder from the DataFrame
sind = np.where(fdf['fname'] == '7"')
# Extract the first element, which is the Folder ID
sind = int(sind[0])
# Using this Folder ID, query for the releases in that folder
sevenlist = me.collection_folders[sind].releases
print(sevenlist.pages)
# for item in me.collection_folders[sind].releases:
#     print(item)

# TODO: Need to write the entire collection to a single list 