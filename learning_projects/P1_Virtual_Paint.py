import cv2
import numpy as np

vid = cv2.VideoCapture(0)
vid.set(3, 512)
vid.set(4, 384)
vid.set(10,150)

count = 0
myPoints=[]

def drawOnCanvas(points):
    for point in points:
        cv2.circle(imgResult, (point[0],point[1]), 10, point[2], cv2.FILLED)


def getContours(img):
    contours,hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x=y=w=h=0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        cv2.drawContours(imgResult,cnt,-1,(255,0,0),3)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,.02*peri,True)
        # cv2.drawContours(imgResult, approx, -1, (255, 0, 0), 10)
        x, y, w,h = cv2.boundingRect (approx)
    return x+w//2,y

def findColor(img,my_Colors):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    points =[]
    # print (len(my_Colors))
    for att in my_Colors:
        # print (color)
        lower = np.array (att[0:3])
        upper = np.array(att[3:6])
        mask = cv2.inRange (imgHSV, lower, upper)
        x,y = getContours(mask)
        if x!=0 and y!=0:
            point = [x,y,att[6]]
            points.append(point)
        cv2.circle(imgResult,(x,y),10, att[6], cv2.FILLED)
    return points


my_Colors = [[175, 133, 150, 179, 168, 188,(115, 10, 63)],
             [86,96,78,126,104,143,178,(18, 128, 107)],
             [26,87,92,46,177,212,(40, 84, 35)]]

# ,"pink":[175, 133, 150, 179, 168, 188],
#               "skin":[0, 100, 130, 19, 197, 130],
#               "Navy Blue":[110, 126, 37, 117, 212, 138],

while True:
    success, img = vid.read()
    imgResult = img.copy()
    newPoints = findColor(img,my_Colors)
    if len(newPoints)!=0:
        myPoints+=newPoints
    if (len(myPoints)!=0):
        drawOnCanvas(myPoints)
    cv2.imshow("Video", imgResult )
    if cv2.waitKey(1) & 0xFF == ord('r'):
        print ("regenerated")
        myPoints=[]
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # cv2.rectangle(imgResult,(0,200),(640,300),(148, 73, 209),cv2.FILLED)
        # cv2.putText(imgResult,"Painting Saved", (150,256), cv2.FONT_HERSHEY_DUPLEX, 2, (152, 245, 71), 2)
        cv2.imwrite("scanned/Virtual_Paint/Painting_"+str(count)+".jpg",imgResult)
        cv2.imshow("Video", imgResult )
        print ("saved")
        cv2.waitKey(500)
        myPoints=[]
        count += 1