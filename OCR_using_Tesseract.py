import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"

###################
width=720//2
height=1520//2
path="WhatsApp Image 2022-03-05 at 2.53.38 PM.jpeg"
###################

# create boxes around every character
# detect every char
def imgToBoxes(img):
    config= r'--oem 3 --psm 6 outputbase digits'
    # predefined function which gives coordinates of every character
    element=pytesseract.image_to_boxes(img,config=config)
    ele_info=[]
    for ele in element.splitlines():
        # each ele is a information of type string (space seperated)
        ele_info=ele.split(" ")
        print (ele_info)
        # ele_info = [char,LeftCorner, height-lowerHeight, rightCorner, height-upperHeight, __]
        val=ele_info[0]
        x1,y1,x2,y2=int(ele_info[1]),int(ele_info[2]),int(ele_info[3]),int(ele_info[4])
        cv2.rectangle (img,(x1,height-y1),(x2,height-y2),(52,125,14),2)
        cv2.putText(imgBlank,val,(x1,height-y1) ,cv2.FONT_HERSHEY_COMPLEX,.37,(150,208,46),1)

#detect in form of string
def imgToData(img):
    # config= r'--oem 3 --psm 6 outputbase digits'
    f = open("1st","w+")
    # inbuilt function
    element=pytesseract.image_to_data(img)
    ele_info=[]
    for x,ele in enumerate(element.splitlines()):
        # print (ele)
        ### ele[0] gives the headings of data (what does the other ele holds in what order)
        if (x!=0):
            # ele is in the form of string contanin 12 info
            ele_info = ele.split()
            # print (ele_info)
            if (len(ele_info)==12):
                # ele_info = [level	page_num	block_num	par_num	line_num	word_num	left	top	width	height	conf	text]
                val=ele_info[11]
                # print (val,end=" ")
                f.write(val+" ")
                x1,y1,x2,y2=int(ele_info[6]),int(ele_info[7]),int(ele_info[8]),int(ele_info[9])
                cv2.rectangle (imgBlank,(x1,y1),(x1+x2,y2+y1),(52,125,14),2)
                print (imgBlank.shape)
                cv2.putText(imgBlank,val,(x1,y1) ,cv2.FONT_HERSHEY_COMPLEX,1,(150,208,46),1)
    f.close()


# trying to extract digits for sudoku but didn't worked
def clickDigit(img):
    imgBlank = np.zeros_like(img)

    imgToData(img)
    # cv2.imshow("original",img)
    # cv2.imshow("Text",imgBlank)
    # cv2.waitKey(0)


img = cv2.imread(path.format(1))
# img = cv2.imread("InQuestion/Screenshot_2021-11-22-22-11-15-90.jpg")
img = cv2.resize(img,(width,height))
imgBlank=np.zeros_like(img)
# print (pytesseract.image_to_string(img))

# imgToBoxes(img)
imgToData(img)

# cv2.rectangle (img,(5,5),(410,90),(52,125,14),2)

cv2.imshow("öriginal",img)
cv2.imshow("Text",imgBlank)
cv2.waitKey(0)