
from os import walk
import os
import natsort
import numpy as np
from PIL import Image

class VideoFileManager:
    def __init__(self, save_folder, save_delta=30, savetype='jpg'):

        # set up saving directory.
        self.save_folder = save_folder
        os.mkdir( self.save_folder )
        os.chmod( self.save_folder, 0o777 )

        self.save_iter = 0 # SET_0 , SET_1 , ...
        self.image_iter = 0 # counts how many images in SET_0 and iterates to SET_1 when save_delta has been reached.
        self.save_delta = save_delta
        # set up initial set to save (SET_0)
        os.mkdir( self.save_folder + '/' + 'SET_' + str(self.save_iter) )
        os.chmod( self.save_folder + '/' + 'SET_' + str(self.save_iter), 0o777 )
        self.base_save_dir = self.save_folder + '/' + 'SET_'

        #self.savetype = findsavetype(savetype) #Todo --> link save type to dictionary of functions.
    
    def save_image(self, image, image_name, iterate_image=True, check_iterate_folder=True):
        curr_savename = self.base_save_dir + str(self.save_iter) + '/' + image_name
        
        self.save_jpg( image, curr_savename )

        if iterate_image:   self.image_iter = self.image_iter + 1
        if check_iterate_folder:     self.check_iterate_folder()


    def check_iterate_folder(self):
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

#loading 
class PredictionFileManager(VideoFileManager):
    def __init__(self, load_folder, save_folder, save_delta=30, savetype='jpg', saving_images=False):
        super().__init__(save_folder, save_delta, savetype)      
        self.saving_images = saving_images      
        self.load_folder = load_folder

        self.iterated_directories = [ ]
        self.image_library = [ ]
        self.current_dir = 'SET_0' #current read directory.
        self.image_read_iter = 0 # 0 from 'SET_0' and so on
        self.image_to_read = None # this COULD just be self.image_iter, but it makes logic of updating the image library easier.

    def save_misc(self, text_to_save, savename):
        current_save_directory = self.base_save_dir + str(self.save_iter) + '/' + savename
        with open(current_save_directory + ".txt", 'w') as write_prediction:
            for line_of_text in text_to_save:
                write_prediction.write("%s\n" % str(line_of_text) )
        
        if not self.saving_images:
            self.image_iter = self.image_iter + 1
            self.check_iterate_read_folder()
            self.check_iterate_folder()
    
    def check_iterate_read_folder(self):
        if self.image_iter >= self.save_delta:
            self.iterated_directories.append( self.current_dir )
            self.image_read_iter = self.image_read_iter + 1
            self.current_dir = 'SET_' + str(self.image_read_iter)
            
           # self.image_iter = self.image_iter - 29 #TODO check 29
           # self.image_to_read = self.image_to_read - 29
            
    def update_image_library(self):
        #TODO test this case with empty directories.
        if self.image_to_read is None:
            temp = []
            for(dirpath, dirnames, filenames) in walk(self.load_folder):
                if len(filenames) is not 0:
                    temp.extend([ dirpath + '/' + x for x in filenames ])
            if len(temp) is not 0:
                self.image_library = natsort.natsorted(temp)
                self.image_to_read = 0
        else:
            if self.image_to_read > (len(self.image_library)): #only update if we need to.
                temp = []
                for(dirpath, dirnames, filenames) in walk(self.load_folder):
                    temp.extend([ dirpath + '/' + x for x in filenames ])
                    self.image_library = temp
        

    # RETURN:
        # [None, None] or [ image_filepath, image_timestamp_name ], where both are strings.
    def get_new_image(self):
        curr_image = None
        image_timestamp_name = None
        if self.image_to_read is not None:
            if self.image_to_read < len(self.image_library):
                curr_image = self.image_library[self.image_to_read]
                self.image_to_read = self.image_to_read + 1
                image_timestamp_name = curr_image
                image_timestamp_name = image_timestamp_name.replace(self.load_folder + '/' + self.current_dir  + '/', '')
                image_timestamp_name = image_timestamp_name.replace('.jpg', '')
            else:
                print(" waiting on more images... ")
        return curr_image, image_timestamp_name