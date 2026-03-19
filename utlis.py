import cv2
import pyperclip as pc
import numpy as np

## TO STACK ALL THE IMAGES IN ONE WINDOW
def stackImages(imgArray,scale,lables=[]):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
            hor_con[x] = np.concatenate(imgArray[x])
        ver = np.vstack(hor)
        ver_con = np.concatenate(hor)
    else:
        for x in range(0, rows):
            imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        hor_con= np.concatenate(imgArray)
        ver = hor
    if len(lables) != 0:
        eachImgWidth= int(ver.shape[1] / cols)
        eachImgHeight = int(ver.shape[0] / rows)
        #print(eachImgHeight)
        for d in range(0, rows):
            for c in range (0,cols):
                cv2.rectangle(ver,(c*eachImgWidth,eachImgHeight*d),(c*eachImgWidth+len(lables[d][c])*13+27,30+eachImgHeight*d),(255,255,255),cv2.FILLED)
                cv2.putText(ver,lables[d][c],(eachImgWidth*c+10,eachImgHeight*d+20),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)
    return ver

def reorder(myPoints):

    myPoints = myPoints.reshape((4, 2)) # REMOVE EXTRA BRACKET
    myPointsNew = np.zeros((4, 1, 2), np.int32) # NEW MATRIX WITH ARRANGED POINTS
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]  #[0,0]
    myPointsNew[3] =myPoints[np.argmax(add)]   #[w,h]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] =myPoints[np.argmin(diff)]  #[w,0]
    myPointsNew[2] = myPoints[np.argmax(diff)] #[h,0]

    return myPointsNew

def rectContour(contours):

    rectCon = []
    max_area = 0
    for i in contours:
        area = cv2.contourArea(i)
        if area > 50:
            peri = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i, 0.02 * peri, True)
            if len(approx) == 4:
                rectCon.append(i)
    rectCon = sorted(rectCon, key=cv2.contourArea,reverse=True)
    return rectCon

def getCornerPoints(cont):
    peri = cv2.arcLength(cont, True) # LENGTH OF CONTOUR
    approx = cv2.approxPolyDP(cont, 0.02 * peri, True) # APPROXIMATE THE POLY TO GET CORNER POINTS
    return approx

def splitImages(img, tipohoja):
    if tipohoja == 1:
        img = cv2.resize(img,(600,600))
        img1 = img[38:572,35:144]
        img2 = img[38:572,184:296]
        img3 = img[38:572,335:445]
        img4 = img[38:572,485:597]
        img1 = cv2.resize(img1,(100,600))
        img2 = cv2.resize(img2,(100,600))
        img3 = cv2.resize(img3,(100,600))
        img4 = cv2.resize(img4,(100,600))
        return img1 , img2 , img3, img4
    if tipohoja == 0:
        img = cv2.resize(img,(600,600))
        img1 = img[6:598,30:119]
        img2 = img[6:598,150:239]
        img3 = img[6:598,270:359]
        img4 = img[6:598,390:479]
        img5 = img[6:598,510:599]
        img1 = cv2.resize(img1,(100,600))
        img2 = cv2.resize(img2,(100,600))
        img3 = cv2.resize(img3,(100,600))
        img4 = cv2.resize(img4,(100,600))
        img5 = cv2.resize(img5,(100,600))
        return img1 , img2 , img3, img4, img5


def splitBoxes(img):
    imgs = splitImages(img, tipohoja=0)
    boxes=[]
    for i in imgs:
        i = cv2.resize(i,(100,600))
        rows = np.vsplit(i,24) 
        for r in rows:
            cols= np.hsplit(r,4)
            for box in cols:

                boxes.append(box)
    
    return boxes

def drawGrid(imge,tipohoja,questions):
    imgs = splitImages(imge,tipohoja)
    for img in imgs:
        secW = int(img.shape[1]/4)
        secH = int(img.shape[0]/questions)
        for i in range (0,questions):
            pt1 = (0,secH*i)
            pt2 = (img.shape[1],secH*i)
            pt3 = (secW * i, 0)
            pt4 = (secW*i,img.shape[0])
            cv2.line(img, pt1, pt2, (255, 255, 0),2)
            cv2.line(img, pt3, pt4, (255, 255, 0),2)
    if tipohoja == 0:
        imgres = cv2.hconcat([imgs[0],imgs[1],imgs[2],imgs[3],imgs[4]])
    if tipohoja == 1:
        imgres = cv2.hconcat([imgs[0],imgs[1],imgs[2],imgs[3]])  
    return imgres

def showAnswers(imge,tipohoja,myIndex,grading,ans,questions,choices=4):
     imgs = splitImages(imge,tipohoja)
     counter = -1
     for img in imgs:
        secW = int(img.shape[1]/choices)
        secH = int(img.shape[0]/questions)
        counter = counter+1
        for x in range(0,questions):
            myAns= myIndex[(x+(questions*counter))]   
            cX = (myAns * secW) + secW // 2
            cY = (x * secH) + secH // 2
            if grading[(x+(questions*counter))]==1:
                myColor = (0,255,0)
                cv2.rectangle(img,(myAns*secW,x*secH),((myAns*secW)+secW,(x*secH)+secH),myColor,cv2.FILLED)
                cv2.circle(img,(cX,cY),7,myColor,cv2.FILLED)
            else:
                myColor = (0,0,255)
                cv2.rectangle(img, (myAns * secW, x * secH), ((myAns * secW) + secW, (x * secH) + secH), myColor, cv2.FILLED)
                cv2.circle(img, (cX, cY),7, myColor, cv2.FILLED)
                # CORRECT ANSWER
                myColor = (255, 0, 0)
                correctAns = ans[(x+(questions*counter))]
                cv2.circle(img,((correctAns * secW)+secW//2, (x * secH)+secH//2),
                5,myColor,cv2.FILLED)
     if tipohoja == 0:
         imgres = cv2.hconcat([imgs[0],imgs[1],imgs[2],imgs[3],imgs[4]])
     if tipohoja == 1:
         imgres = cv2.hconcat([imgs[0],imgs[1],imgs[2],imgs[3]])
     return imgres

def copyfun(ans):
    lenAns = len(ans)
    StringAns = ""
    for x in range(0,lenAns):
        StringAns = StringAns + str(ans[x])+"\t"

    print(StringAns)
    return StringAns  

def copy(Stringan):
    pc.copy(Stringan)


def ansTuple(res,resnum):
    resun = int(resnum)
    respuestas = []
    for x in range(0,resun):
        if res[x] == "a":
            respuestas.append(0)
        elif res[x] == "b":
            respuestas.append(1) 
        elif res[x] == "c":
            respuestas.append(2) 
        elif res[x] == "d":
            respuestas.append(3) 
    return respuestas

def the120inator(res):
    lenres = len(res)
    print(res)
    if lenres != 120:
        for x in range (lenres,120):
            res.append(0)
    print("nuevo res", res)
    return res

def the120ans(len, grade):
    len = int(len)
    grade2 = []
    for x in range (0,len):
        grade2.append(grade[x])
    return grade2

