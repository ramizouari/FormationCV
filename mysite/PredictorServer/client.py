# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 00:14:45 2021

@author: Rami
"""

import socket

import cv2
import numpy as np
import pickle

def receive(client_socket):
     data=b""
     while True:
        packet = client_socket.recv(4096)
        if not packet: break
        data += packet
     return pickle.loads(data)


def client_program():
    video = cv2.VideoCapture(0)  
    host = socket.gethostname()  # as both code is running on same pc
    port = 5000  # socket server port number
    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server

    while True:
        _,frame = video.read()
        if _ == 0:
            break
        h,w = frame.shape[:2]
        
     
        client_socket.send(pickle.dumps(frame))  # send message
        detections=receive(client_socket)
       
        for i in range(0 , detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            if confidence > 0.5:
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (x,y,W,H) = box.astype("int")
                #print("sx: ",x,"ex",w,"sy",y,"ey",h)
    
                crop = frame[y:H, x:W]
                rgb = cv2.cvtColor(crop, cv2.COLOR_BGR2RGB)
                resize = cv2.resize(rgb, (224, 224))
                [r,x,y,W,H]=receive(client_socket)
                label = "Mask Detected" if r else "No Mask Detected"
                color = (0,255,0) if label == "Mask Detected" else (0,0,255)
                cv2.putText(frame, label, (x,y-10), cv2.FONT_HERSHEY_SIMPLEX,0.6,
                            color,2)
                cv2.rectangle(frame,(x,y),(W,H),color,2)
                response = [label,x,y,W,H]
        cv2.imshow("Output",frame)
        key = cv2.waitKey(1)
        if key == ord('w'):
            break
        
        if key == ord('q'):
            break
    cv2.imwrite("out.jpeg",frame)
    video.release()
    cv2.destroyAllWindows()
    client_socket.close()  # close the connection
#client_program()