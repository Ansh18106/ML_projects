import cv2
import numpy as np

wImg = 613
hImg = 980

path1 = "resources/lab scan.jpg"
path2 = "resources/MM news.jpg"
path3 = "resources/document-formatting-example-1-mobile.jpg"
path4="resources/DocumentScan.jpg"
path5 = "resources/shapes2.png"
# vid = cv2.VideoCapture(0)
# vid.set(3, wImg)
# vid.set(4, hImg)
# vid.set(10,150)


def getContours(img):
    biggest = np.array([])
    areaMax=0
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    print (contours)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 3)
        print (area)
        # if area >500:
        cv2.drawContours(imgThres,cnt,-1,(255,0,0),3)
        peri = cv2.arcLength(cnt,True)
        # print (peri)
        approx = cv2.approxPolyDP(cnt,.02*peri,True)
        if area>areaMax and len(approx)==4:
            biggest = approx
            areaMax = area
    print (biggest)
    cv2.drawContours(imgContour, biggest, -1, (255, 0, 0), 20)
    return biggest

def reorder (myPoints):
    myPoints = myPoints.squeeze()
    myPointsSum = myPoints.sum(1)
    myPointsDiff = np.diff(myPoints,axis=1)
    print (myPointsSum)
    myPointsRet = np.zeros((4,1,2),np.int32)
    myPointsRet[0] = myPoints[np.argmin(myPointsSum)]
    myPointsRet[3] = myPoints[np.argmax(myPointsSum)]
    myPointsRet[1] = myPoints[np.argmin(myPointsDiff)]
    myPointsRet[2] = myPoints[np.argmax(myPointsDiff)]
    return myPointsRet

def getWarp(img,biggest):
    # pts1 = np.float32 ([[2001/4,1609/4],[2689/4,1641/4],[477/4,3465/4],[2113/4,3837/4]])
    print (biggest.shape)
    pts1 = np.float32 (biggest)
    pts2 = np.float32([[0,0],[wImg,0],[0,hImg],[wImg,hImg]])

    matrix = cv2.getPerspectiveTransform(pts1,pts2)
    imageOutput = cv2.warpPerspective (img,matrix,(wImg,hImg))
    return imageOutput

def preProcessing(img):
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(5,5),1)
    # bilateral = cv2.bilateralFilter(imgGray, 15, 75, 75)
    imgCanny = cv2.Canny(imgBlur,200,200)
    kernel = np.ones((5,5))
    imgDial = cv2.dilate(imgCanny,kernel,iterations=1)
    imgThres = cv2.erode (imgDial,kernel,iterations=2)
    return imgCanny,imgDial,imgThres


img = cv2.imread(path3)
img = cv2.resize(img,(hImg,wImg))
imgContour = img.copy()
imgCanny, imgDial, imgThres = preProcessing(img)
biggest = getContours(imgCanny)
biggest = biggest.squeeze()
biggest = reorder(biggest)
if (biggest.size!=0):
    imgWarped = getWarp(img,biggest)
    cv2.imshow("Warped",imgWarped)


cv2.imshow("original",img)
cv2.imshow("canny",imgCanny)
cv2.imshow("dialated",imgDial)
cv2.imshow("threshold",imgThres)
cv2.imshow("Contours",imgContour)
cv2.waitKey(0)
# while True:
#     success, img = vid.read()
#     # img = cv2.resize(img,(hImg,wImg))
#     imgThres = preProcessing(img)
#     cv2.imshow("imgThres", imgThres)
#     cv2.imshow("Video", img)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break