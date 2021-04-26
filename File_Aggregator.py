# This program is meant to reconstruct a user's folder and file structure from
# a Windows OneCare Backup. Once you have unzipped the folders into a directory,
# you point the program to that directory and it will automatically
# reconstruct the folder structure and COPY the files from the zip folders to 
# a new "Reconstructed Dir" folder. 

# David Swartzendruber, 2021

import os
import pathlib
from shutil import copyfile
import argparse as ap

parser = ap.ArgumentParser(description='Reconstruct OneCare backups.')

parser.add_argument('src', 
                    type=str, 
                    help='Full path to OneCare backup of interest')

parser.add_argument('dst', 
                    type=str, 
                    help='Full path to store unpacked backup info')

args = parser.parse_args()

ROOT_PATH = args.src
RECV_FULL = args.dst

file_list = []
dir_list =[]

print("Source: %s" % args.src)
print("Destination: %s" % args.dst)


# Walk folders to find all files and paths, store in list
def create_lists():
    for paths, dirs, files in os.walk(ROOT_PATH):
        for item in files:
            file_list.append(os.path.join(paths,item))
        for item in dirs:
            p = pathlib.Path(os.path.relpath(os.path.join(paths,item),ROOT_PATH))
            dir_list.append(pathlib.Path(*p.parts[1:]))
    return [dir_list,file_list]

# Create folder structure to place recovered items in
def create_structure(dir_in):
    if not os.path.exists(RECV_FULL):
        os.mkdir(RECV_FULL)
    else:
        print("Recovery dir already made!")

    for item in dir_in:
        try:
            os.makedirs(os.path.join(RECV_FULL,item), exist_ok=True)
        except OSError as e:
            print("Directory `%s` can not be created" % item)

# Move files to new folder structure
def move_files(file_in):
    for item in file_in:
        p = pathlib.Path(item)
        a = RECV_FULL + "\\" + str(pathlib.Path(*p.parts[4:]))
        copyfile(item,a)

def main():
    [dir_out,file_out] = create_lists()
    print("Lists created...")
    create_structure(dir_out)
    print("Structure rebuild completed...")
    move_files(file_out)
    print("\n\n=============================\nScript completed!\n=============================\n")

if __name__ == "__main__":
    main()