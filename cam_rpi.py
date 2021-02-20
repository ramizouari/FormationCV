# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:34:21 2021

@author: Rami
"""
import requests
import cv2
import numpy as np
import threading
import os

#Main Class
class CameraRecorderWithPredictor():
    #Initialisation with a temporary file path tmp_name & server url
    def __init__(self,tmp_name,url):
        self.response=""
        self.tmp_name=tmp_name
        self.url=url
        self.ready=True
        pass
    
    #Send an image to the server
    def post(self):
        with open(self.tmp_name,mode="rb") as f:
            img=f.read()      
        test_req=requests.post(self.url,files={"image":img})
        if test_req.ok:
            self.response=test_req.text
        else:
            self.response=""
        self.ready=True

    def loop(self):
#Use PC Camera
        video=cv2.VideoCapture("rtsp://cam:1234@192.168.43.1:8320/h264_ulaw.sdp")
        while True:
            _, frame = video.read()
#Write Image to temporary file
            cv2.imwrite(self.tmp_name,frame)
#If No request is on progress, send a new request on a new thread
            if self.ready:
                self.thread=threading.Thread(target=self.post)
                self.thread.start()
                self.ready=False
#If there is no response
            if self.response!="":
#Else we will convert out response
                for line in self.response.split("\n"):
#The response is of the format x:y:w:h:m for each line
                    (x,y,w,h,has_mask)=[int(s) for s in line.split(':')]
                    has_mask=bool(has_mask)
#Create a Crop for the detected face 
                    crop = frame[y:h, x:w]
                    label = "Mask Detected" if has_mask else "No Mask Detected"
                    color = (0,255,0) if label == "Mask Detected" else (0,0,255)
#Add Mask Detection text for each detected face
                    cv2.putText(frame, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.6,
                                color,2)
#Add Mask Detection color for each detected face
                    cv2.rectangle(frame,(x,y),(w,h),color,2)
#Wait for key input, if 'q' is clicked, we will exit
            key = cv2.waitKey(1)    
            if key == ord('q'):
                break
            cv2.imshow("Camera",frame)
#Release The used camera
        video.release()
        cv2.destroyAllWindows()
#Delete The temporary file
        os.remove(self.tmp_name)
    pass
#http://40.115.35.164:8000/predict/detailed
recorder= CameraRecorderWithPredictor(
    "test.jpeg", "http://localhost:8000/predict/detailed")
recorder.loop()
