import requests
import time

import cv2
import urllib 
import numpy as np

latency =  0.05 # 5 milliseconds request

capture = cv2.VideoCapture('http://10.1.10.158:8000/stream.mjpg', cv2.CAP_DSHOW)

total_found = 0

while(True):
    t_start = time.time()
    ret, frame = capture.read()
    if frame is not None:
        print(frame.shape)
        total_found = total_found + 1
   # print(frame.shape)
   # total_found = total_found + 1
    print(total_found)
    t_end = time.time()
    print(t_end - t_start) 

   # r = requests.get('http://10.1.10.158:8000/stream.mjpg')
    # print(len(r))
    # print(r)
    # print('--')
    time.sleep(latency)

