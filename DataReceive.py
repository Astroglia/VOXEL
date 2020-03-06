import requests
import time

import cv2
import urllib 
import numpy as np
import queue
import threading
import os

import FileHelper

# latency =  0.05 # 5 milliseconds request

# #capture = cv2.VideoCapture('http://10.1.10.158:8000/stream.mjpg')
# capture = cv2.VideoCapture('http://10.42.0.156:8000/stream.mjpg')

# total_found = 0

# Framelist = []

# t_total = 0
# while(True):
#     t_start = time.time()
#     ret, frame = capture.read()
#     received_request = requests.get('http://10.42.0.156:8000/index.html')
#     print(received_request.headers)
#     if frame is not None:
#         #Framelist.append(frame)
#         print(type(received_request.headers['Date']))
#         total_found = total_found + 1
#     t_end = time.time() 
#     t_total = t_total + (t_end - t_start)

#     if total_found >= 100:
#         print(total_found)
#         print(t_total)
#         total_found = 0
#         t_total = 0

    # print(total_found)
    # t_end = time.time()
    # print(t_end - t_start) 

   # r = requests.get('http://10.1.10.158:8000/stream.mjpg')
    # print(len(r))
    # print(r)
    # print('--')
   # time.sleep(latency)

class RPiVideoStream:
    def __init__(self, pi_address, framerate, save_folder):
        self.pi_address = pi_address
        self.base_page_address = 'http://' + self.pi_address + '/index.html'
        self.video_stream_address = 'http://' + self.pi_address + '/stream.mjpg'
        self.framerate = framerate

        self.file_helper = FileHelper.VideoFileManager(save_folder = save_folder)
        
        self.streaming = False
        self.streaming_data = queue.Queue()
        # TODO saverate
    
    def start_streaming_pipeline(self):
        stream_thread = threading.Thread(target=self.continuous_stream)
        save_thread = threading.Thread(target=self.continuous_save)

        stream_thread.start()
        save_thread.start()

    def continuous_stream(self):
        self.streaming = True
        
        capture_object = cv2.VideoCapture(self.video_stream_address)

        while(self.streaming):
            ### GET STREAMING DATA & HEADER INFORMATION
            ret, frame = capture_object.read()
            received_request = requests.get(self.base_page_address)
            if frame is not None:

                frame = cv2.resize(frame, dsize=(368, 368), interpolation=cv2.INTER_CUBIC) #resize
                self.set_streaming_data( [frame, received_request.headers['tstamp'] ])
            time.sleep(0.001)
    
    def continuous_save(self):
        while(self.streaming):
            [ stream_data, timestamp ] = self.get_streaming_data()
            self.file_helper.save_image(stream_data, timestamp)
            time.sleep(0.001)


    def set_streaming_data(self, data):
        self.streaming_data.put(data)
    def get_streaming_data(self):
        return self.streaming_data.get()
    def stop_streaming(self):
        self.streaming = False


######################################################################################### 

    #TODO hmm, make it work (ping module no longer exists in python3?)
    def check_connections(self):
        import ping, socket
        connections_good = True
        try:
            ping.verbose_ping(self.base_page_address, count=1)
            delay = ping.Ping(self.base_page_address, timeout=2000).do()
        except socket.error:
            connections_good = False
            print("ping error when trying to connect to: ", self.base_page_address)
        try:
            ping.verbose_ping(self.video_stream_address, count=1)
            delay = ping.Ping(self.video_stream_address, timeout=2000).do()
        except socket.error:
            connections_good = False
            print("ping error when trying to connect to: ", self.video_stream_address)
        return connections_good