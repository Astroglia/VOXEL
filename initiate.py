import DataReceive
import DataProcess
import time
# http://10.42.0.156:8000/
# '10.42.0.156:8000' #eth0 @ Lab
# '10.42.0.111:8000' #eth0 @Ashmore, Second RPi3B+

PHOTO_FOLDER = 'test_stream'
PREDICTION_RESULT_FOLDER = 'test_stream_result'


### SAVE DELTAS ON RECEIVE AND PREDICT OBJECT MUST BE THE SAME CURRENTLY.
#receive_object_1 = DataReceive.RPiVideoStream(pi_address='10.42.0.111:8000', framerate=30, save_folder=PHOTO_FOLDER)
#time.sleep(1)
predict_object_1 = DataProcess.ActivePredict(search_folder='./' + PHOTO_FOLDER, save_folder=PREDICTION_RESULT_FOLDER)

predict_object_1.start_prediction_pipeline(verbose=True)
time.sleep(5)
#receive_object_1.start_streaming_pipeline()

while(True):
    time.sleep(1)
#receive_object_1.stop_streaming()
predict_object_1.stop_predicting(finish_processing=False)
