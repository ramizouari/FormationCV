# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:34:21 2021

@author: Rami
"""
import requests
import cv2
import numpy as np


video=cv2.VideoCapture(0)

while True:
    _, frame = video.read()
    h,w = frame.shape[:2]
    cv2.imwrite("test.jpeg",frame)
    url="http://40.115.35.164:8000/predict"
    with open("test.jpeg",mode="rb") as f:
        img=f.read()
        test_res=requests.post(url,files={"image":img})
        if test_res.ok:
            print(test_res.text)
        else:
            print("Error")
    key = cv2.waitKey(1)    
    if key == ord('q'):
        break

video.release()
cv2.destroyAllWindows()