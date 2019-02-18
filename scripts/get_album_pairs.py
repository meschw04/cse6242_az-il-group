import csv
import pandas as pd
import ast

only_albums_with_covers = False

# read in csv
with open('albums_data.csv') as csvfile:
    df = pd.read_csv('albums_data.csv')
    scanned_albums = df['AlbumName'].tolist()
    album_pairs = []
    for a, b, c in zip(df['AlbumName'], df['Artist'], df['SimilarAlbums']):
        rowlist = []
        rowlist += ast.literal_eval(c)
        for q in rowlist:
            if only_albums_with_covers is False or q[1] in scanned_albums:
                album_pairs.append([b + "-- " + a, q[0] + "-- " + q[1]])
csvfile.close()

album_pairs.sort(key=lambda x: x[0])

seen = set()
similarListNoDuplicates = []
for line in album_pairs:
    if line[0] < line[1]:
        compare = tuple(line)
    else:
        reverseLine = [line[1], line[0]]
        compare = tuple(reverseLine)
    if compare not in seen:
        seen.add(compare)
        similarListNoDuplicates.append(line)

with open('album_pairs.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(similarListNoDuplicates)
csvfile.close()