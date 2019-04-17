from keras.models import load_model
import matplotlib.pyplot as plt
import sys
try:
    sys.path.remove('/opt/ros/kinetic/lib/python2.7/dist-packages')
    import cv2
except:
    pass
import numpy as np
import urllib
import os

def import_models():
    try:
	del load_encoder
	del load_decoder
	load_encoder = load_model('records_auto-enc_v1.h5')
	load_decoder = load_model('records_auto-dec_v1.h5')
        return load_encoder, load_decoder
    except:
        load_encoder = load_model('records_auto-enc_v1.h5')
	load_decoder = load_model('records_auto-dec_v1.h5')
        return load_encoder, load_decoder


def run_autoencoder(url1, url2):
    #load_encoder = load_model('records_auto-enc_v1.h5')
    #load_decoder = load_model('records_auto-dec_v1.h5')
    #ae = load_model('records_ae_v1.h5')
    load_encoder, load_decoder = import_models()
    pic1 = urllib.request.urlopen(url1).read()
    filename1 = 'url1.png'
    with open(filename1,'wb') as f:
        f.write(pic1)
    cv2.imwrite(filename1,cv2.resize(cv2.imread(filename1),(128,128)))
    test1 = cv2.resize(cv2.imread(filename1),(128,128))

    pic2 = urllib.request.urlopen(url2).read()
    filename2 = 'url2.png'
    with open(filename2,'wb') as f:
        f.write(pic2)
    cv2.imwrite(filename2,cv2.resize(cv2.imread(filename2),(128,128)))
    test2 = cv2.resize(cv2.imread(filename2),(128,128))
    
    f, axarr = plt.subplots(2, 6, figsize=(16,6))
    axarr[0,0].imshow(cv2.cvtColor(np.uint8(test1), cv2.COLOR_BGR2RGB))
    
    interp_space = np.linspace(0.1,0.9,9)
    
    enc1 = load_encoder.predict(np.array([test1])/255.)
    enc2 = load_encoder.predict(np.array([test2])/255.)
    
    for i in range(len(interp_space)):
       interp_01 = np.array(enc1)+interp_space[i]*(np.array(enc2)-np.array(enc1))
    
       out_interp_01 = load_decoder.predict(interp_01)
       #print(out_interp_01.tolist())
       if i<5:
           axarr[0,i%5+1].imshow(cv2.cvtColor(np.uint8(out_interp_01[0]*255), cv2.COLOR_BGR2RGB))
       else:
           axarr[1,i%5].imshow(cv2.cvtColor(np.uint8(out_interp_01[0]*255), cv2.COLOR_BGR2RGB))
    
    axarr[1,4].imshow(cv2.cvtColor(np.uint8(test2), cv2.COLOR_BGR2RGB))
    axarr[1,5].set_axis_off()
    plt.savefig("./static/img/ae_output.png")
    os.remove('url1.png')
    os.remove('url2.png')
    plt.clf()
    print('Image Saved at '+str(os.getcwd())+'./static/img/ae_output.png')

#Example:
#run_autoencoder("https://lastfm-img2.akamaized.net/i/u/300x300/6df20949c1cf44edc451581e314f064e.png",\
#                "https://lastfm-img2.akamaized.net/i/u/300x300/9f9c4d5ee17a4762c79c26886e320727.png")
