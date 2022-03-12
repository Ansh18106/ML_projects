import cv2
import numpy as np

red_factor = .5
width=360
height=240


def stackFrames (imgArr,factor):
    rows = len(imgArr)
    cols= len(imgArr[0])
    rowsAvailable= isinstance(imgArr[0],list)

    if rowsAvailable:
        width=imgArr[0][0].shape[1]
        height=imgArr[0][0].shape[0]
        ver = np.zeros((0, width*cols, 3), np.uint8)
        hor = [np.zeros((height, 0, 3), np.uint8)]*rows
        for x in range(0,rows):
            for y in range(0,cols):
                if imgArr[x][y].shape[:2] == 3:imgArr[x][y] = cv2.resize(imgArr[x][y], (0,0), None, factor, factor)
                else:imgArr[x][y]= cv2.resize(imgArr[x][y], (width, height), None, factor, factor)
                if len(imgArr[x][y].shape) == 2:imgArr[x][y] = cv2.cvtColor(imgArr[x][y], cv2.COLOR_GRAY2BGR)
                hor[x] = np.hstack((hor[x],imgArr[x][y]))
            ver=np.vstack((ver,hor[x]))
    else:
        width=imgArr[0].shape[1]
        height=imgArr[0].shape[0]
        hor = np.zeros((height,width,3),np.uint8)
        for x in range(0,rows):
            if imgArr[x].shape[:2] == 3:imgArr[x] = cv2.resize(imgArr[x], (0,0), None, factor, factor)
            else:imgArr[x]= cv2.resize(imgArr[x], (width, height), None, factor, factor)
            if len(imgArr[x].shape) == 2:imgArr[x] = cv2.cvtColor(imgArr[x], cv2.COLOR_GRAY2BGR)
            hor = np.hstack((hor,imgArr[x]))
        ver = hor
    return ver

img = cv2.imread("resources/sample_sky.jpg")
imgBlank = np.zeros_like(img)
img = cv2.resize(img,(width,height))
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
imgBlur=cv2.GaussianBlur (imgGray,(7,7),1)
imgCanny = cv2.Canny (imgBlur,50,50)
imgStack=stackFrames([[img,imgHSV,imgCanny],[img,imgBlank,imgBlur]],red_factor)
cv2.imshow("stacked",imgStack)
cv2.waitKey(0)
