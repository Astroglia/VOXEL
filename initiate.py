import DataReceive
import DataProcess
import time
# http://10.42.0.156:8000/
# '10.42.0.156:8000' #eth0 @ Lab
# '10.42.0.111:8000' #eth0 @Ashmore, Second RPi3B+

receive_object_1 = DataReceive.RPiVideoStream('10.42.0.111:8000', 30, save_folder='test')
predict_object_1 = DataProcess.ActivePredict('test', 'test_processed')

receive_object_1.start_streaming_pipeline()
predict_object_1.start_prediction_pipeline()

time.sleep(10)
receive_object_1.stop_streaming()
predict_object_1.stop_predicting(finish_processing=False)
