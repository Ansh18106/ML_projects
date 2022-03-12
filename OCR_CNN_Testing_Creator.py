import numpy as np
import cv2
import pickle
from tensorflow.keras.models import load_model

###################
width=640
height=480
path="testSample/{}.jpg"
###################

# pickle_in=open("learning_integers.p","rb")
model = load_model('myModel.h5')
# print  (model)

def preProcessing(img):
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # img=cv2.equalizeHist(img)
    img=img/255
    return img

# imgOriginal = cv2.imread(path.format(i))

def testDigit(image):
    img = np.asarray(image)
    # cv2.imshow("index", img)
    # cv2.waitKey(0)
    img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
    img=cv2.resize(img,(28,28))
    img = img / 255
    img=img.reshape(1,28,28,1)
    # GET PREDICTION
    predictions = model.predict(img)
    classIndex = model.predict_classes(img)
    probabilityValue = np.amax(predictions)
    # print (probabilityValue, classIndex)
    ## SAVE TO RESULT
    if probabilityValue > 0.8:
        return classIndex[0]
    else:
        return 0


# def testDigit(imgOriginal):
#     img=np.asarray(imgOriginal)
#     img=cv2.resize(img,(32,32))
#     img=preProcessing(img)
#     # cv2.imshow("PreProcessed",img)
#     img=img.reshape(1,32,32,1)
#
#     classIndex=int(model.predict_classes(img))
#     preidction = model.predict(img)
#     probVal=np.amax(preidction)
#     if (probVal>0.8):return classIndex,probVal
#     return 0,0



