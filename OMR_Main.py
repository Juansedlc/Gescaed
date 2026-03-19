import cv2
import numpy as np
import utlis
import normalizerhoja

########################################################################
ans= [2, 2, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 3, 2, 1, 0, 1, 2, 0, 2, 0, 0, 1, 1, 2, 2, 3, 3, 2, 2, 1, 1, 0, 0, 1, 1, 2, 2, 1, 3, 2, 2, 1, 1]
    
def califier(pathImage,ansin):
    tipohoja= 1
    pathImage
    heightImg = 875
    widthImg  = 600
    if tipohoja == 1:
        questions=  60
        columns = 4
    if tipohoja == 0:
        questions=  120
        columns = 5
    choices= 4
    ans = ansin
    print("Respuestas que toma el programa",ans)
     ########################################################################


    img = cv2.imread(pathImage)
    img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
    imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
    imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 
    

    try:
        ## FIND ALL COUNTOURS
        imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
        contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
        cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
        rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
        biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
        
        if biggestPoints.size != 0:
            # BIGGEST RECTANGLE WARPING
            biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
            cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
            #cv2.imshow("image",imgBigContour)
            #cv2.waitKey(0)
            pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
            pts2 = np.float32([[-25, -25],[625, -25], [-25, 625],[625, 625]]) # PREPARE POINTS FOR WARP
            matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
            imgWarpColored = cv2.warpPerspective(img, matrix, (600, 600)) # APPLY WARP PERSPECTIVE
            # APPLY THRESHOLD
            imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
            imgThresh = cv2.threshold(imgWarpGray, 210, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE
            if tipohoja == 0:
                 boxes = utlis.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES
            if tipohoja == 1:
                boxes = normalizerhoja.img_normalizer(imgThresh)
            index = len(boxes)//columns
            boxes1 = []
            boxes1.append(boxes[:index])
            for x in range(1,columns):
                boxes1.append(boxes[(index*x):(index*(x+1))])
            countR=0
            countC=0
            myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX

            for boxes in boxes1:
                for image in boxes:
                #    cv2.imshow(str(countR)+str(countC),image)
                #    cv2.waitKey(0)
                    totalPixels = cv2.countNonZero(image)
                    myPixelVal[countR][countC]= totalPixels
                    countC += 1
                    if (countC==choices):countC=0;countR +=1
            # FIND THE USER ANSWERS AND PUT THEM IN A LIST
            myIndex=[]
            for x in range (0,questions):
                arr = myPixelVal[x]
                myIndexVal = np.where(arr == np.amax(arr))
                myIndex.append(myIndexVal[0][0])
            # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
            grading=[]
            for x in range(0,questions):
                if ans[x] == myIndex[x]:
                    grading.append(1)
                else:grading.append(0)
            # DISPLAYING ANSWERS
        
            imgWarpColored = utlis.drawGrid(imgWarpColored,tipohoja,(int(questions/columns))) # DRAW GRID
            imgRawDrawings = np.zeros_like(imgWarpColored) # NEW BLANK IMAGE WITH WARP IMAGE SIZE
            imgRawDrawings = utlis.showAnswers(imgRawDrawings,tipohoja, myIndex, grading, ans,int(questions/columns)) # DRAW ON NEW IMAGE
            imgWarpColored = cv2.addWeighted(imgWarpColored, 1, imgRawDrawings, 1,0)
    except:
        imageArray = ([img,imgGray,imgCanny,imgContours],
                        [imgBlank, imgBlank, imgBlank, imgBlank])
        
    return grading, imgWarpColored