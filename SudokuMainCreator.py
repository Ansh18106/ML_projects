print('Setting UP')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import cv2
import numpy as np
from OCR_CNN_Testing import *
# from OCR_using_Tesseract import *
from stackingFunc import *
###################
width=360
height=760
path="InQuestion/Q{}.jpg"
###################

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

def getContour(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    maxArea,biggestCnt=0,contours[0]
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print (area)
        cv2.drawContours(imgOriginal,cnt,-1,(255,0,0),3)
        peri = cv2.arcLength(cnt,True)
        # print (peri)
        approx = cv2.approxPolyDP(cnt,.02*peri,True)
        objCor = len(approx)
        # print (objCor,approx)
        if (objCor==4 and area>maxArea):
            # cv2.drawContours(imgOriginal, cnt, -1, (255, 0, 0), 2)
            # print (approx)
            approx1=approx
            approx=reorder(approx)
            # print(approx1==approx)
            x, y, w,h = cv2.boundingRect (approx)
            pts1 = np.float32 ([[x,y],[w+x,y],[x,y+h],[x+w,y+h]])
            pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])

            matrix = cv2.getPerspectiveTransform(pts1,pts2)
            ques= cv2.warpPerspective (img,matrix,(w,h))
            maxArea, biggestCnt, maxWidth, maxheight, maxX, maxY =area, cnt, w, h, x, y
    cv2.drawContours(imgOriginal, biggestCnt, -1, (255, 0, 0), 2)

    return ques, maxWidth, maxheight, maxX, maxY

def createArr(x_,y,w,h):
    pts1 = np.float32 ([[x,y],[w+x,y],[x,y+h],[x+w,y+h]])
    pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    quesImg= cv2.warpPerspective (imgGray,matrix,(w,h))
    quesImg=cv2.resize(quesImg,(540,540))
    # quesImg = cv2.cvtColor(quesImg, cv2.COLOR_BGR2GRAY)
    print (quesImg.shape)
    cv2.imshow("quesImg",quesImg)
    cv2.waitKey(0)
    indexVal = [[0] * 9 for _ in range(9)]
    prob = [[0] * 9 for _ in range(9)]
    imgMat = [[img] * 9 for _ in range(9)]
    rows = np.vsplit(quesImg,9)
    for i,r in enumerate(rows):
        cols= np.hsplit(r,9)
        for j,box in enumerate(cols):
            indexVal[i][j]=testDigit(box)
            print (indexVal[i][j],end=" ")
        print ("||")
            # boxes.append(box)
    # for i in range(9):
    #     x=x_
    #     for j in range(9):
    #         image = image[3.5:image.shape[0] - 3.5, 3.5:image.shape[1] - 3.5]
    #         # print (image.shape)
    #         # indexVal[i][j],prob[i][j]=testDigit(imgWarpColored)
    #         indexVal[i][j]=testDigit(image)
    #         # clickDigit(imgVal)
    #
    #         # cv2.imshow("index"+str(i)+str(j),imgVal)
    #         # cv2.imread("Q3_({},{})".format(i,j),imgVal)
    #         imgMat[i][j] = imgVal
    #         print (indexVal[i][j],end=" ")
    #         x+=w
    #     print ("||")
    #     y+=h
    # # stackImgs (imgMat)
    return indexVal,prob

img=cv2.imread(path.format(3))
imgOriginal=cv2.resize(img,(width,height))
imgGray=cv2.cvtColor(imgOriginal,cv2.COLOR_BGR2GRAY)
imgCanny=cv2.Canny(imgOriginal,50,50)
ques,widthQ,heightQ,x,y=getContour(imgCanny)
indexVal,prob = createArr(x,y,widthQ,heightQ)
# imgWarpColored = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY)

#             pts1 = np.float32 ([[x,y],[x+w,y],[x,y+h],[x+w,y+h]])
#             pts2 = np.float32([[0,0],[w,0],[0,h],[w,h]])
#             matrix = cv2.getPerspectiveTransform(pts1,pts2)
#             imgVal= cv2.warpPerspective (imgOriginal,matrix,(w,h))
#             image = cv2.cvtColor(imgVal,cv2.COLOR_BGR2GRAY)
# for i in range(9):
#     for j in range(9):
#         print (prob[i][j],end=" " )
#     print ("||")

# cv2.imshow("Original",imgOriginal)
cv2.imshow("ques",ques)
# cv2.imwrite("scanned/Sudoku_Ques_1.jpg", ques)
cv2.waitKey(0)


# 2 3 0 6 0 0 2 0 0 ||
# 7 0 0 0 2 0 0 1 0 ||
# 0 0 0 0 1 2 0 0 0 ||
# 0 0 2 0 4 0 0 0 0 ||
# 1 0 0 0 0 0 0 0 0 ||
# 0 0 0 0 2 0 0 3 1 || 0
# 0 7 0 7 7 7 0 7 7 ||
# 4 4 0 0 4 3 0 0 8 ||
# 0 5 0 0 0 4 0 1 0 ||

# 2 3 0 6 0 0 2 0 3 ||
# 7 0 0 0 2 0 0 1 0 ||
# 0 0 0 0 1 2 0 0 0 ||
# 7 7 7 7 2 7 7 7 7 ||
# 1 2 0 2 0 0 0 0 0 ||
# 7 4 7 0 2 7 4 3 0 ||
# 0 7 0 7 7 7 7 7 7 || 4
# 0 0 5 0 4 0 0 0 8 ||
# 1 0 0 0 0 4 0 4 0 ||