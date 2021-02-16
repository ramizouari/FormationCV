import requests
import cv2
import sys
import pickle

def test_post():
    url="http://40.115.35.164:8000/predict"
    img=cv2.imread("ai_meme.jpg")
    test_res=requests.post(url,files={"image":pickle.dumps(img)})
    if test_res.ok:
        print(test_res.text)
    else:
        print("Error")
        
        
def test_post2(filename):
    url="http://40.115.35.164:8000/predict"
    with open(filename,mode="rb") as f:
        img=f.read()
        test_res=requests.post(url,files={"image":img})
        if test_res.ok:
            print(test_res.text)
        else:
            print("Error")