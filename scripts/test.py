import urllib.request
import matplotlib.pyplot as plt
import json
import numpy as np
import cv2
#from scipy.ndimage import imread
my_api_key = "57ee3318536b23ee81d6b27e36997cde"

haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_alt.xml')
sift = cv2.xfeatures2d.SIFT_create()


def write_cover_png(address,filename,show=False):
    pic = urllib.request.urlopen(address).read()
    with open(filename,'wb') as f:
        f.write(pic)
    if show:
        picture = plt.imread(filename)
        test1 = cv2.imread(filename)
#        gray_img = cv2.cvtColor(test1, cv2.COLOR_BGR2GRAY)
        (kps, descs) = sift.detectAndCompute(test1,None)
        #FACE STUFF
#        faces = haar_face_cascade.detectMultiScale(gray_img,1.1,1) #initially 1.1,1
#        print('Num Faces: '+str(len(faces)))
        print(descs.shape)
        plt.figure()
        plt.imshow(picture)
        plt.show()


#address = 'https://lastfm-img2.akamaized.net/i/u/300x300/94e53cb2ea84a37cc5b2ba6acc6d6dd8.png'
#pic = urllib.request.urlopen(address).read()
#with open('test.png','wb') as f:
#    f.write(pic)
#https://lastfm-img2.akamaized.net/i/u/300x300/94e53cb2ea84a37cc5b2ba6acc6d6dd8.png
    
#write_cover_png(address,'test.png')

classic_rock_artists = open('classic_rock_artists.txt', 'r').read().split('\n')


#"http://ws.audioscrobbler.com/2.0/?method=artist.getTopAlbums&artist=Spock%27s+Beard&api_key="+my_api_key+"&format=json"
artist = 'U2'
address = "http://ws.audioscrobbler.com/2.0/?method=artist.getTopAlbums&artist="+\
            artist+"&api_key="+my_api_key+"&format=json"
#data = urllib.request.urlopen(address).read()
data = json.loads(urllib.request.urlopen(address).read())
print(len(data['topalbums']['album']))
for i in data['topalbums']['album'][:10]:
    if i['name'] != '(null)':
        print(i['name'])
        print(i['image'][-1]['#text'])
        print(i['playcount'])
        print('')
        try:
            write_cover_png(i['image'][-1]['#text'],'test.png',show=True)
        except ValueError:
            pass
#classic_rock_artists[0]