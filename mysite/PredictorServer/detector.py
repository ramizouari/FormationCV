import cv2
import numpy as np
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model


#Loading Facial Recognition Model
print("[INFO] loading facial recognition model...")
prototxtPath = "PredictorServer/deploy.prototxt"
weightsPath = "PredictorServer/res10_300x300_ssd_iter_140000_fp16.caffemodel"
net = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)

#Loading Mask Detection Model
print("[INFO] loading face mask detector model...")
model = load_model("PredictorServer/mask_detect.model")
'''
    This function will accept a frame, and count the number of detections and number of 
    detected masks
    1. It will read at first the original image, preprocess it to a form understandable by
    opencv, then detect faces with a trained opencv deep neural network
    If a face is detected, it will output the boundaries of an adequate crop 
    containing the face
    2. For each detected face with high probability (>0.5), it will select t
    
'''
def detect(frame,retCrops=False):  
#Height & Weight
    h,w = frame.shape[:2]
    #Preprocess image to the 
    blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 117.0, 123.0),False,False)
    print("[INFO] computing face detections...")
    net.setInput(blob)
    detections = net.forward()
    detection_count=0
    mask_count=0
    crops=[]
    for i in range(0 , detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (x,y,W,H) = box.astype("int")
            #print("sx: ",x,"ex",w,"sy",y,"ey",h)
            crop = frame[y:H, x:W]
            rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
            resize = cv2.resize(rgb, (224, 224))
            img_array = img_to_array(resize)
            process = preprocess_input(img_array)
            face = np.expand_dims(process, axis=0)
            (mask, withoutMask) = model.predict(face)[0]
            detection_count=detection_count+1
            if mask>withoutMask:
                mask_count=mask_count+1
            if retCrops:
                crops.append([x,y,W,H,1 if mask>withoutMask else 0])

    return np.array(crops) if retCrops else (detection_count,mask_count) 
        

