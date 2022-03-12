# lines to hide some expected errors in cmd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2
import numpy as np
from OCR_CNN_Testing import *
from stackingFunc import *
from solveSudoku import *

###################
width=360
height=760
path="InQuestion/Q{}.jpg"
###################

# to place the corners at their right place (upper left should be at upper left and lower right at lower right and so on)
def reorder (myPoints):
    myPoints = myPoints.squeeze()
    myPointsSum = myPoints.sum(1)
    myPointsDiff = np.diff(myPoints,axis=1)
    # print (myPointsSum)
    myPointsRet = np.zeros((4,1,2),np.int32)
    myPointsRet[0] = myPoints[np.argmin(myPointsSum)]
    myPointsRet[3] = myPoints[np.argmax(myPointsSum)]
    myPointsRet[1] = myPoints[np.argmin(myPointsDiff)]
    myPointsRet[2] = myPoints[np.argmax(myPointsDiff)]
    return myPointsRet

# function to crop 'img' of height, width = h, w from the coordinates (x,y) of 'img'
def crop(x,y,w,h,img):
    pts1 = np.float32 ([[x,y],[w+x,y],[x,y+h],[x+w,y+h]])
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    img= cv2.warpPerspective (img,matrix,(w,h))
    return img

# function ot get biggest contour which is the ques
def getContour(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    maxArea,biggestCnt=0,contours[0]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(imgOriginal,cnt,-1,(255,0,0),3)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,.02*peri,True)
        objCor = len(approx)
        # ques image must have 4 corners and the biggest area
        if (objCor==4 and area>maxArea):
            #ques img needed to be reorder
            approx=reorder(approx)

            # cropping image ques
            x, y, w,h = cv2.boundingRect (approx)
            ques = crop(x,y,w,h,img)
            maxArea, biggestCnt, maxWidth, maxheight, maxX, maxY =area, cnt, w, h, x, y
    cv2.drawContours(imgOriginal, biggestCnt, -1, (255, 0, 0), 2)

    # return ques,w, h, x, y
    return ques, maxWidth, maxheight, maxX, maxY

def createArr(quesImg):
    # resizing image to a factor of 9 so that it can be divided into 81 squares
    # enlarging image enough to predict the integer value
    quesImg = cv2.resize(quesImg,(540,540))
    indexVal = [[0] * 9 for _ in range(9)]
    prob = [[0] * 9 for _ in range(9)]
    rows = np.vsplit(quesImg,9)
    for i,r in enumerate(rows):
        cols= np.hsplit(r,9)
        for j,box in enumerate(cols):
            indexVal[i][j], prob[i][j]=testDigit(box)
            print (indexVal[i][j],end=" ")
        print ("||")
    return indexVal,prob

## image reading and preprocessing:
img=cv2.imread(path.format(1))
imgOriginal=cv2.resize(img,(width,height))

#  to find question contour canny image is used
imgCanny=cv2.Canny(imgOriginal,50,50)
ques,w, h, x, y=getContour(imgCanny)

# converting the RBG img to GRAY img
imgGray = cv2.cvtColor(imgOriginal, cv2.COLOR_BGR2GRAY)

# cropping GRAY img to ques img
quesImg = crop(x, y, w, h, imgGray)

# creating grid of 9*9
grid,prob = createArr(quesImg)
quesGrid = grid
for i in range(9):
    for j in range(9):
        s = grid[i][j]
        quesGrid[i][j] = s


# image in ques
ques = cv2.resize(ques,(360,360))

# solve and print solution
print ("\nSolution")
grid = solveSudoku(grid)

# creating blank img
quesImg = np.zeros((360,360,3),dtype=np.uint8)
ansImg = np.zeros((360,360,3),dtype=np.uint8)
x=4
for j in range(9):
    y=4
    for i in range(9):
        if (prob[i][j]!=1):
            cv2.rectangle(quesImg, (x, y), (x + 32, y + 32), (207, 161, 32), 2)
            cv2.putText(quesImg, str(grid[i][j]), (x + 10, y + 27), cv2.FONT_HERSHEY_COMPLEX, 1, (52, 125, 145), 1)
        else:
            cv2.rectangle(ansImg, (x, y), (x + 32, y + 32), (37, 161, 207), 2)
            cv2.putText(ansImg, str(grid[i][j]), (x + 10, y + 27), cv2.FONT_HERSHEY_COMPLEX, 1, (125, 52, 145), 1)
        y+=40
    x+=40

# stack images
images = [[ques,quesImg, ansImg]]
stackImgs(images)

cv2.waitKey(0)
