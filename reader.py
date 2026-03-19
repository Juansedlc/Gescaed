import cv2
from pyzbar.pyzbar import decode
from tkinter import filedialog as fd 
import numpy as np

def reader(path):
        img = cv2.imread(path)
        img = img[25:1625,0:1275]
        
        img = cv2.resize(img, (1200, 1500)) # RESIZE IMAGE
        rows = np.vsplit(img,3) 
        cols= np.hsplit(rows[0],2)
        cols[-1] = cv2.resize(cols[-1], (600,600)) # RESIZE IMAGE 
        rows = np.vsplit(cols[-1],2) 
        cols= np.hsplit(rows[0],2)
        qr = cols[-1]
        #qr = qr[50:300,0:250]
        clean_im = cv2.medianBlur(qr, 5)  # Apply median blur for reducing noise
        #small_clean_im = cv2.resize(clean_im, (512, 512), interpolation=cv2.INTER_AREA) 
       # cv2.imshow("a",clean_im)
        #cv2.waitKey(0)
        for barcode in decode(clean_im):
            myData = barcode.data.decode("utf-8")
        myData = myData.split(" ,")
        return myData[0]

