"""
Commands- 
dlink: python3 parallel_firmware_checker.py -p /shared/firmware-images/validset/dlink_latest -c dlink -l /shared/firmware-images/binwalk-result/dlink-logs
"""

import argparse
import os
import subprocess
import re
import logging
import json
import time

binwalk_folder = "/shared/firmware-images/binwalk-result"
job_completion_index = os.getenv('JOB_COMPLETION_INDEX')

parser = argparse.ArgumentParser(description='Enter the path for the file directory')
parser.add_argument("-p", "--path", help = "Please enter the path of the directory")
parser.add_argument("-c", "--customer", help = "Please enter the name of the customer you're processing")
parser.add_argument("-l", "--logpath", help = "Please enter the folder path for logging")
args = parser.parse_args()

log_file = os.path.join(args.logpath, str(job_completion_index) + ".log")

logging.basicConfig(
        filename=log_file,
        filemode='a',
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s : %(message)s',
        level=logging.DEBUG,
        datefmt='%Y-%m-%d %H:%M:%S')


def create_test_folder(path):
    test_folder_path = os.path.join(path, "test-folder")
    if not os.path.exists(test_folder_path):
        os.makedirs(test_folder_path)
    return test_folder_path

def get_firmware_path(job_completion_index):
    customer_file_path = os.path.join(binwalk_folder, args.customer + ".json")
    # logging.debug("JSON file path: %s", customer_file_path)
    with open(customer_file_path, "r") as fp:
        customer_firmware_paths = json.load(fp)
    
    return customer_firmware_paths[job_completion_index]

def move_zip_files_to_test_folder(processing_file_name, test_folder_path):
    # logging.debug("copying file from %s to %s", processing_file_path, test_folder_path)
    # os.system("cp %s %s" % (processing_file_path, test_folder_path))
    os.system("cd %s && cp %s %s" % (args.path, processing_file_name, test_folder_path))

def move_zip_file_to_docker_container(processing_file_name, target_folder="."):
    logging.debug("cp %s %s", os.path.join(args.path, processing_file_name), target_folder)
    # os.system("cd %s && cp %s %s" % (args.path, processing_file_name, target_folder))
    os.system("cp %s %s" % (os.path.join(args.path, processing_file_name), target_folder))

def binwalk_helper(test_folder_path, processing_file_name):
    os.system("cd %s && binwalk -eM %s" % (test_folder_path, processing_file_name))

def binwalk_docker_helper(processing_file_name):
    os.system("binwalk -eM %s" %(processing_file_name))

def is_binary_file(extracted_folder_path):
    for r, d, f in os.walk(extracted_folder_path):
        for file in f:
            file_path = os.path.join(r, file)
            if re.match(r'.*bin\/sh.*', file_path) or re.match(r'.*bin\/busybox.*', file_path):
                return True
    return False


if __name__ == "__main__":
    try:
        processing_file_path = get_firmware_path(job_completion_index)
        # logging.debug("This is the processing file path: %s", processing_file_path)

        processing_file_name = processing_file_path.split("/")[-1]
        logging.debug("This is the processing file name: %s", processing_file_name)

        # test_folder_path = create_test_folder(args.path)
        # logging.debug("Folder path: %s", test_folder_path)


        
        # logging.debug("Extracted Folder Path: %s", extracted_folder_path)

        move_zip_file_to_docker_container(processing_file_name)
        # move_zip_files_to_test_folder(processing_file_name, test_folder_path)

        binwalk_docker_helper(processing_file_name)
        # binwalk_helper(test_folder_path, processing_file_name)

        extracted_folder_path = os.path.join("_" + processing_file_name + ".extracted")

        if os.path.exists(extracted_folder_path):
            logging.debug("File path exists")
        else:
            logging.debug("File path doesn't exit")

        if is_binary_file(extracted_folder_path):
            logging.debug("%s is a firmware image", extracted_folder_path)
        else:
            logging.debug("%s is not a firmware image", extracted_folder_path)

        time.sleep(100)

    except Exception as Argument:
        logging.exception("Error has occured, log message below:")
