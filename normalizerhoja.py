import numpy as np
import cv2

def img_normalizer(img):
#img = cv2.imread("qrs\\prueba tresh.jpg")
    img = img[38:572,0:600]
    img =  cv2.resize(img,(600,600))
    quest = []
    colums = np.hsplit(img,4)
    for c in colums:
        print(c.shape)
        filas = np.vsplit(c,15)
        for f in filas:
            quest.append(f)

    i = 0    
    boxes = []
    for b in quest: 
        var = b
        var = b[2:40,30:150]
        var = cv2.resize(var,(120,38))
        circles = np.hsplit(var,4)
        for c in circles:
            boxes.append(c)  
    size = len(boxes)
    print(size)
#while i < size:
##    cv2.imshow("casilla n: "+ str(i+1), boxes[i])
 #   cv2.waitKey(0)
 #   i= i+1
    return boxes