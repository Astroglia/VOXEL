import DataReceive
import time

# http://10.42.0.156:8000/
# '10.42.0.156:8000' #eth0 @ Lab
receive_object_1 = DataReceive.VideoStreamStorage('10.42.0.156:8000', 30, 'bananas')
#receive_object_1.check_connections()
receive_object_1.start_streaming_pipeline()

time.sleep(10)
receive_object_1.stop_streaming()
