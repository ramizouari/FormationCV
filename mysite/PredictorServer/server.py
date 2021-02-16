# -*- coding: utf-8 -*-
"""
Created on Tue Jan 12 00:13:04 2021

@author: Rami
"""

import socket
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model
import numpy as np
import cv2
import pickle

def receive(client_socket):
     data=b""
     while True:
        packet = client_socket.recv(4096)
        if not packet: break
        data += packet
     return pickle.loads(data)

def server_program():
    prototxtPath = "deploy.prototxt"
    weightsPath = "res10_300x300_ssd_iter_140000_fp16.caffemodel"
    net = cv2.dnn.readNetFromCaffe(prototxtPath, weightsPath)
    
    print("[INFO] loading face mask detector model...")
    model = load_model("mask_detect.model")
    # get the hostname
    host = socket.gethostname()
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        
        frame=receive(conn)
        blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300),(104.0, 117.0, 123.0),False,False)
        print("[INFO] computing face detections...")
        h,w = frame.shape[:2]
        if not blob:
            continue
        net.setInput(blob)
        detections = net.forward()
        conn.send(pickle.dumps(detections))
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
                r = mask > withoutMask
                response = [r,x,y,W,H]
                conn.send(pickle.dumps(response))
                #cv2.imshow("crop",process)
    conn.close()
server_program()