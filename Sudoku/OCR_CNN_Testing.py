import numpy as np
import cv2
from tensorflow.keras.models import load_model

###################
width=640
height=480
path="testSample/{}.jpg"
###################

model = load_model('myModel.h5')

def preProcessing(img):
    img = np.asarray(img)
    img = img[4:img.shape[0] - 4, 4:img.shape[1] - 4]
    img=cv2.resize(img,(28,28))
    img = img / 255
    img=img.reshape(1,28,28,1)
    return img

def testDigit(image):
    img = preProcessing(image)
    predictions = model.predict(img)
    classIndex = model.predict_classes(img)
    probabilityValue = np.amax(predictions)
    if probabilityValue > 0.8:
        return classIndex[0], probabilityValue
    else:
        return 0, probabilityValue

