import urllib.request
import matplotlib.pyplot as plt
import json
import numpy as np
import cv2
import csv
import pandas as pd
import ast
#from scipy.ndimage import imread

my_api_key = "57ee3318536b23ee81d6b27e36997cde"


def write_cover_png(address,filename,show=False):
    pic = urllib.request.urlopen(address).read()
    with open(filename,'wb') as f:
        f.write(pic)
    if show:
        picture = plt.imread(filename)
        test1 = cv2.imread(filename)
#        gray_img = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
#        (kps, descs) = sift.detectAndCompute(test1,None)
        #FACE STUFF
#        faces = haar_face_cascade.detectMultiScale(gray_img,1.1,1) #initially 1.1,1
#        print('Num Faces: '+str(len(faces)))
#        print(descs.shape)
        plt.figure()
        plt.imshow(picture)
        plt.show()

def get_similar_songs(song, artist, limit=10):
    similar_song_info = 'http://ws.audioscrobbler.com/2.0/?'+\
                        'method=track.getsimilar&'+\
                        'artist='+'%20'.join(artist.split(' '))+\
                        '&track='+'%20'.join(song.split(' '))+\
                        '&api_key='+my_api_key+\
                        '&format=json'
    
    similar_song_data = json.loads(urllib.request.urlopen(similar_song_info).read())
    related_num = min(limit,len(similar_song_data['similartracks']['track']))
    similar_songs = [i['name'] for i in \
                     similar_song_data['similartracks']['track'][:related_num]]
    similar_song_artists = [i['artist']['name'] for i \
                            in similar_song_data['similartracks']['track'][:related_num]]
    return similar_songs,similar_song_artists


def get_similar_albums(initial_artist,initial_album):
    album_address = 'http://ws.audioscrobbler.com/2.0/?'+\
                        'method=album.getInfo&'+\
                        'api_key='+my_api_key+\
                        '&artist='+'%20'.join(initial_artist.split(' '))+\
                        '&album='+'%20'.join(initial_album.split(' '))+\
                        '&format=json'
                        
    data = json.loads(urllib.request.urlopen(album_address).read())
    
    song_list = [i['name'] for i in data['album']['tracks']['track']]
    play_count = []
    for i in song_list:
        song_info = 'http://ws.audioscrobbler.com/2.0/?method=track.getinfo&'+\
                        'artist='+'%20'.join(initial_artist.split(' '))+\
                            '&track='+'%20'.join(i.split(' '))+\
                            '&api_key='+my_api_key+\
                            '&format=json'
        song_data = json.loads(urllib.request.urlopen(song_info).read())
        play_count.append(int(song_data['track']['playcount']))
    
    
    most_popular_song = song_list[play_count.index(max(play_count))]
    
    similar_songs,similar_song_artists = get_similar_songs(most_popular_song,initial_artist,limit=25)
    
    #print(similar_songs)
    #print(similar_song_artists)
    similar_albums_li = []
    similar_artists_li = []
    try:
        for i in range(len(similar_song_artists)):
        #    print(similar_songs[i],similar_song_artists[i])
            similar_song_query = 'http://ws.audioscrobbler.com/2.0/?method=track.getinfo&'+\
                                'artist='+'%20'.join(similar_song_artists[i].split(' '))+\
                                '&track='+'%20'.join(similar_songs[i].split(' '))+\
                                '&api_key='+my_api_key+\
                                '&format=json'
            similar_song_data = json.loads(urllib.request.urlopen(similar_song_query).read())
            if similar_song_artists[i] == similar_song_data['track']['album']['artist']:
                if similar_song_data['track']['album']['title'] != initial_album:
                    similar_albums_li.append(similar_song_data['track']['album']['title'])
                    similar_artists_li.append(similar_song_data['track']['album']['artist'])
            else:
                pass
    except KeyError:
        pass
    return list(set(zip(similar_artists_li,similar_albums_li)))

def get_album_info(initial_artist,initial_album):
    album_query = 'http://ws.audioscrobbler.com/2.0/?method=album.getinfo&'+\
                    'api_key='+my_api_key+\
                    '&artist='+'%20'.join(initial_artist.split(' '))+\
                    '&album='+'%20'.join(initial_album.split(' '))+\
                    '&format=json'
    album_data = json.loads(urllib.request.urlopen(album_query).read())
    playcount = album_data['album']['playcount']
    listeners = album_data['album']['listeners']
    tags = [j['name'] for j in album_data['album']['tags']['tag']]
    image_link = album_data['album']['image'][-1]['#text']
    pic = urllib.request.urlopen(image_link).read()
    #Decide filename!
    filename = 'album_images/'+initial_album+'_'+initial_artist+'.png'
    with open(filename,'wb') as f:
        f.write(pic)
    cv2.imwrite(filename,cv2.resize(cv2.imread(filename),(128,128)))
    similar = get_similar_albums(initial_artist,initial_album)
    return [initial_album,initial_artist,playcount,listeners,similar,image_link,filename,tags]


initial_artist = 'Michael Jackson'
initial_album = 'Thriller'


#print(get_album_info(initial_artist,initial_album))

stop_num = 1000

i = len(pd.read_csv('albums_data.csv'))
while i<stop_num:
    if i == 0:
    
        with open('albums_data.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            print(initial_artist,initial_album)
            t=get_album_info(initial_artist,initial_album)
            writer.writerow(t)
            i+=1
        csvfile.close()
    
    else:
        try:
            df = pd.read_csv('albums_data.csv')
            scanned_albums = df['AlbumName'].tolist()
            unscanned_albums = []
            for q in df['SimilarAlbums'].tolist():
                unscanned_albums+=ast.literal_eval(q)
            not_original=True
            while not_original:
                selected_album = unscanned_albums[int(np.random.choice(range(len(unscanned_albums)),1))]
                if selected_album[1] in scanned_albums:
                    pass
                else:
                    not_original=False
            with open('albums_data.csv','a') as csvfile:
                writer = csv.writer(csvfile)
                print(selected_album[0],selected_album[1])
                writer.writerow(get_album_info(selected_album[0],selected_album[1]))
                i+=1
            csvfile.close()
        except (ValueError,KeyError):
            pass
        
#        raise ValueError
#        with open('albums_data.csv','a') as csvfile:
        





