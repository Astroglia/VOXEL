from os import walk
import natsort

parent_folder = './test'

files = []
already_iterated = ['SET_0', 'SET_1' ]
for(dirpath, dirnames, filenames) in walk(parent_folder):
    for i in range(len(already_iterated)):
        print(dirnames)
        dirnames = [ x for x in dirnames if already_iterated[i] not in x ]
    # print(dirpath)
    # print(dirnames)
    # print(filenames)
    filenames = [ dirpath + '/' + x for x in filenames]
    files.extend( filenames )
  #  break

files = natsort.natsorted(files)
print(files)