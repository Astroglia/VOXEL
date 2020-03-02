
import os
import numpy as np
from PIL import Image

class VideoFileManager:
    def __init__(self, save_folder, save_delta=30, savetype='jpg'):
        self.save_folder = save_folder
        #set up saving directory 
        os.mkdir( self.save_folder )
        os.chmod( self.save_folder, 0o777 )

        self.save_iter = 0
        self.image_iter = 0
        self.save_delta = save_delta
        os.mkdir( self.save_folder + '/' + 'SET_' + str(self.save_iter) )
        os.chmod( self.save_folder + '/' + 'SET_' + str(self.save_iter), 0o777 )
        self.base_save_dir = self.save_folder + '/' + 'SET_'

        #self.savetype = findsavetype(savetype) #Todo --> link save type to dictionary of functions.
    
    def save_image(self, image, image_name):
        curr_savename = self.base_save_dir + str(self.save_iter) + '/' + image_name
        
        self.save_jpg( image, curr_savename )

        self.image_iter = self.image_iter + 1
        self.check_reset()

    def check_reset(self):
        if self.image_iter >= self.save_delta:
            self.image_iter = 0
            self.save_iter = self.save_iter + 1
            os.mkdir( self.save_folder + '/' + 'SET_' + str(self.save_iter) )
            os.chmod( self.save_folder + '/' + 'SET_' + str(self.save_iter), 0o777 )

    def save_numpy(self, image, filename):
        np.save( filename + '.npy' , image,  allow_pickle = True)
        os.chmod( filename + '.npy', 0o777 )

    def save_jpg(self, image, filename):
        im = Image.fromarray( image )
        im.save(filename + '.jpg')
        os.chmod( filename + '.jpg', 0o777 )

    # def findsavetype(file_extension):
    #     if file_extension == 'jpg'

class PredictionFileManager(VideoFileManager):
    def __init__(self, save_folder, save_delta=30, savetype='jpg', saving_images=False):
        super().__init__(save_folder, save_delta, savetype)      
        self.saving_images = saving_images      
    
    def save_misc(self, text_to_save, savename):
        current_save_directory = self.base_save_dir + str(self.save_iter) + '/' + savename
        with open(current_save_directory + ".txt", 'w') as write_prediction:
            for line_of_text in text_to_save:
                write_prediction.write("%s\n" % str(line_of_text) )
        
        if not self.saving_images:
            self.image_iter = self.image_iter + 1
            self.check_reset

# TODO implement me! (file loading for predictions)
    #     from os import walk
    # import natsort

    # parent_folder = './test'

    # files = []
    # already_iterated = ['SET_0', 'SET_1' ]
    # for(dirpath, dirnames, filenames) in walk(parent_folder):

    #     filenames = [ dirpath + '/' + x for x in filenames]
    #     files.extend( filenames )
    # #  break

    # files = natsort.natsorted(files)
    # print(files)