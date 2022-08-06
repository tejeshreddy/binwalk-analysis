"""
Command: python3 firmware_checker.py -p /shared/firmware-images/dlink/dlink-images

"""

import argparse
import os
import subprocess
import re
import logging


# variables
extenstions = ["zip", "ZIP"]
binwalk_folder = "/shared/firmware-images/binwalk-result"

def list_zip_files(path):
    zip_files = []
    files = os.listdir(path)
    files = [path + "/" + file for file in files]

    for file in files:
        if file.rsplit(".")[-1] in extenstions:
            zip_files.append(file)
    return zip_files

def create_test_folder(path):
    test_folder_path = os.path.join(path, "test-folder")
    if not os.path.exists(test_folder_path):
        os.makedirs(test_folder_path)
    return test_folder_path

def move_zip_files_to_test_folder(zip_files, test_folder_path):
    for file in zip_files:
        logging.debug("copying file from %s to %s", file, test_folder_path)
        os.system("cp %s %s" % (file, test_folder_path))

def binwalk_helper(test_folder_path):
    for file in os.listdir(test_folder_path):
        logging.debug("Binwalk for file: %s has started", file)
        os.system("cd %s && binwalk -eM %s" % (test_folder_path, file))
        logging.debug("Binwalk on file: %s completed", file)

def is_binary_file(binary_file_path):
    logging.debug("Started os walk for path: %s", binary_file_path)
    for r, d, f in os.walk(binary_file_path):
        for file in f:
            file_path = os.path.join(r, file)
            logging.debug(file_path)
            if re.match(r'.*bin\/sh.*', file_path) or re.match(r'.*bin\/busybox.*', file_path):
                return True
    return False

def binwalk_validator(test_folder_path):
    print(test_folder_path)

    for file in os.listdir(test_folder_path):
        if file.startswith("_") and file.endswith(".extracted"):
            logging.debug("Found extracted file: %s", file)
            if is_binary_file(os.path.join(test_folder_path, file)):
                with open(os.path.join(binwalk_folder, "confirmed_binaries.txt"), "a") as fp:
                    to_write = os.path.join(test_folder_path, file[1:].replace(".extracted", ""))
                    # to_write = to_write[1:]
                    # to_write = to_write.replace(".extracted", "")
                    fp.write(to_write)
                    fp.write("\n")

if __name__ == "__main__":
    
    log_file = os.path.join(binwalk_folder, "binwalk.log")
    logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')

    parser = argparse.ArgumentParser(description='Enter the path for the file directory')
    parser.add_argument("-p", "--path", help = "Please enter the path of the directory")
    args = parser.parse_args()

    zip_files = list_zip_files(args.path)
    test_folder_path = create_test_folder(args.path)

    # move_zip_files_to_test_folder(zip_files, test_folder_path)
    # binwalk_helper(test_folder_path)
    binwalk_validator(test_folder_path)
