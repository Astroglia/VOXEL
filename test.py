from os import walk
import os
import natsort

parent_folder = './test'

files = []
already_iterated = ['SET_0', 'SET_1' ]

# sets = os.listdir(parent_folder)
# for i in already_iterated: sets = [x for x in sets if i not in x]
# print(sets)
# files = [ ]
# for i in sets:
#   if 

# for i in range(len(sets)):


for(dirpath, dirnames, filenames) in walk(parent_folder):
  print(parent_folder)
  print(dirpath)
  print(filenames)
   # for i in range(len(already_iterated)):
   #     print(dirnames)
   #     dirpath = [ x for x in dirpath if already_iterated[i] not in x ]
    # print(dirpath)
    # print(dirnames)
    # print(filenames)
  filenames = [ dirpath + '/' + x for x in filenames]
  files.extend( filenames )
  #  break

files = natsort.natsorted(files)
print(files)

# print("#####################################################################")
# print(os.listdir(parent_folder))