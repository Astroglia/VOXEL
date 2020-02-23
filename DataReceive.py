import requests
import time

import cv2
import urllib 
import numpy as np

latency =  0.05 # 5 milliseconds request

#capture = cv2.VideoCapture('http://10.1.10.158:8000/stream.mjpg')
capture = cv2.VideoCapture('http://10.42.0.156:8000/stream.mjpg')

total_found = 0

Framelist = []

t_total = 0
while(True):
    t_start = time.time()
    ret, frame = capture.read()
    received_request = requests.get('http://10.42.0.156:8000/index.html')
    print(received_request.headers)
    if frame is not None:
        #Framelist.append(frame)
        print(type(received_request.headers['Date']))
        total_found = total_found + 1
    t_end = time.time() 
    t_total = t_total + (t_end - t_start)

    if total_found >= 100:
        print(total_found)
        print(t_total)
        total_found = 0
        t_total = 0

    # print(total_found)
    # t_end = time.time()
    # print(t_end - t_start) 

   # r = requests.get('http://10.1.10.158:8000/stream.mjpg')
    # print(len(r))
    # print(r)
    # print('--')
   # time.sleep(latency)

