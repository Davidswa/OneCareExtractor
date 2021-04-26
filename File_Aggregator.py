# This program reconstructs a user's folder and file structure from
# a Windows OneCare Backup.

# David Swartzendruber, 2021

import os
import pathlib
from shutil import copyfile
import argparse as ap
from tqdm import tqdm
from zipfile import ZipFile
import glob

parser = ap.ArgumentParser(description='Reconstruct OneCare backups.')

parser.add_argument('src', 
                    type=str, 
                    help='Full path to OneCare backup of interest')

parser.add_argument('dst', 
                    type=str, 
                    help='Full path to store unpacked backup info')

parser.add_argument('-u',
                    '--unzipped',
                    action='store_true',
                    help='Optional, files already unzipped flag')

args = parser.parse_args()

ROOT_PATH = args.src
RECV_PATH = args.dst

file_list = []
dir_list =[]
zip_list = []

#Unzip folders
def unzip_folders():
    files_path = os.path.join(ROOT_PATH,"Files")
    for file in tqdm(glob.glob(files_path + "\*.zip"),desc="Unzipping files"):
        with ZipFile(file,'r') as zipObj:
            zipObj.extractall(RECV_PATH)


# Walk folders to find all files and paths, store in list
def create_lists(path_in):
    for paths, dirs, files in os.walk(path_in):
        for item in files:
            file_list.append(os.path.join(paths,item))
        for item in dirs:
            p = pathlib.Path(os.path.relpath(os.path.join(paths,item),path_in))
            dir_list.append(pathlib.Path(*p.parts[1:]))
    return [dir_list,file_list]

# Create folder structure to place recovered items in
def create_structure(dir_in):
    if not os.path.exists(RECV_PATH):
        os.mkdir(RECV_PATH)
    else:
        print("Recovery dir already made!")

    for item in dir_in:
        try:
            os.makedirs(os.path.join(RECV_PATH,item), exist_ok=True)
        except OSError as e:
            print("Directory `%s` can not be created" % item)

# Move files to new folder structure
def move_files(file_in):
    for item in tqdm(file_in,desc="Copying Files"):
        p = pathlib.Path(item)
        a = RECV_PATH + "\\" + str(pathlib.Path(*p.parts[4:]))
        copyfile(item,a)

# Reconstruct split files
def join_files(path_in):
    pass

def main():
    if(not args.unzipped):
        unzip_folders()
        [dir_out,file_out] = create_lists(RECV_PATH)
        # Do something to eliminate file list of all non- "PART XXX OF"
        # for file in split_list:
        #     join_files(file)

    else:
        [dir_out,file_out] = create_lists(ROOT_PATH)
        print("Lists created...")
        create_structure(dir_out)
        print("Structure rebuild completed...")
        move_files(file_out)

    print("\n=============================\nBackup extraction complete!\n=============================\n")

if __name__ == "__main__":
    main()