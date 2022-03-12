import cv2

cap = cv2.VideoCapture(0)
cap.set(10,1000)
noPlatesCascade = cv2.CascadeClassifier ("resources/haarcascade_russian_car.xml")
minArea = 500
color=(61, 121, 173)
count = 0

while True:
    success, img = cap.read()
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    noPlates = noPlatesCascade.detectMultiScale(imgGray, 1.1, 4)
    for (x, y, w, h) in noPlates:
        area = w*h
        if (area > minArea):
            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText (img,"NumberPlate",(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2 )
            imgRegion = img[y:y+h,x:x+w]
            imgRegion = cv2.resize(imgRegion,(2*w,2*h))
            cv2.imshow("Region",imgRegion)
            print ("got it")

    cv2.imshow("Result",img)
    if cv2.waitKey(1) & 0xFF == ord('s'):
        cv2.rectangle(img,(0,200),(640,300),(148, 73, 209),cv2.FILLED)
        cv2.putText(img,"Scan Saved", (150,256), cv2.FONT_HERSHEY_DUPLEX, 2, (152, 245, 71), 2)
        cv2.imwrite("scanned/No_Plate_Detection/No_Plate_"+str(count)+".jpg",imgRegion)
        cv2.imshow("Result", img)
        cv2.waitKey(500)
        count += 1
    # cv2.waitKey(1)
