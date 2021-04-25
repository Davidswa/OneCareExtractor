# This program is meant to reconstruct a user's folder and file structure from
# a Windows OneCare Backup. Once you have unzipped the folders into a directory,
# you point the program to that directory and it will automatically
# reconstruct the folder structure and COPY the files from the zip folders to 
# a new "Reconstructed Dir" folder. 

# David Swartzendruber, 2021

import os
import pathlib
from shutil import copyfile

ROOT_PATH = "I:\\180541\\BBBB"
RECV_FOLDER_NAME = "Reconstructed Dir"
RECV_FULL = ROOT_PATH + "\\" + RECV_FOLDER_NAME

file_list = []
dir_list =[]

# Walk folders to find all files and paths, store in list
for paths, dirs, files in os.walk(ROOT_PATH):
    for item in files:
        file_list.append(os.path.join(paths,item))
    for item in dirs:
        p = pathlib.Path(os.path.relpath(os.path.join(paths,item),ROOT_PATH))
        dir_list.append(pathlib.Path(*p.parts[1:]))

# Create folder structure to place recovered items in
if not os.path.exists(RECV_FULL):
    os.mkdir(RECV_FULL)
else:
    print("Recovery dir already made!")

for item in dir_list:
    try:
        os.makedirs(os.path.join(RECV_FULL,item), exist_ok=True)
    except OSError as e:
        print("Directory `%s` can not be created" % item)

# Move files to new folder structure
for item in file_list:
    p = pathlib.Path(item)
    a = RECV_FULL + "\\" + str(pathlib.Path(*p.parts[4:]))
    copyfile(item,a)


print("\n\n=============================\nScript completed!\n=============================\n")