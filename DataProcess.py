# prediction class
import FileHelper
import threading, time

import tf_pose

class ActivePredict:
    def __init__(self, search_folder, save_folder):
        self.search_folder = search_folder
        self.file_helper = FileHelper.PredictionFileManager(load_folder=self.search_folder, save_folder = save_folder)
    
        self.predicting = True

        self.base_directory = search_folder

    def start_prediction_pipeline(self, verbose=False):
        active_predict = threading.Thread(target=self.continuous_predict, args=[verbose])
        active_predict.start()

    def stop_predicting(self, finish_processing=False):
        # TODO  implement short stop/long stop
        self.predicting = False

    
    def continuous_predict(self, verbose=False):

        while(self.predicting):
            self.file_helper.update_image_library()
            image_path, image_timestamp_name = self.file_helper.get_new_image()
            if image_path is not None:
                coco_style = tf_pose.infer(image_path)
              #  coco_style = [ 'asdf', 'asdf2']
                self.file_helper.save_misc(coco_style, image_timestamp_name)
                if verbose:
                    print(coco_style)

            time.sleep(0.001)
        
    