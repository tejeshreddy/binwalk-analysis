"""
Usage: - 
dlink: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/dlink-logs/dlink_firmware_images.txt -f /shared/firmware-images/binwalk-result/dlink.json -d /shared/firmware-images/segregated-images/dlink
netgear: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/netgear-logs/netgear_firmware_images.txt -f /shared/firmware-images/binwalk-result/netgear.json -d /shared/firmware-images/segregated-images/netgear
tenda: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/tenda-logs/tenda_firmware_images.txt -f /shared/firmware-images/binwalk-result/tenda.json -d /shared/firmware-images/segregated-images/tenda
tplink: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/tplink-logs/tplink_correct_images.txt -f /shared/firmware-images/binwalk-result/tplink.json -d /shared/firmware-images/segregated-images/tplink
trendnet: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/trendnet-logs/combined_firmware.txt -f /shared/firmware-images/binwalk-result/trendnet.json -d /shared/firmware-images/segregated-images/trendnet
asus: python3 firmware_image_segregator.py -p /shared/firmware-images/binwalk-result/asus-logs/combined_firmware.txt -f /shared/firmware-images/binwalk-result/asus.json -d /shared/firmware-images/segregated-images/asus
"""

import os
import json
import sys
import argparse

parser = argparse.ArgumentParser(description='Enter the path for the file directory')
parser.add_argument("-p", "--path", help="Path of file where all the firmware image paths are present")
parser.add_argument("-f", "--file", help="JSON file where all firmware images are present")
parser.add_argument("-d", "--directory", help="Directory where we should copy the files to")

args = parser.parse_args()

def create_folders(directory_path):
    global correct_folder, incorrect_folder
    correct_folder = os.path.join(directory_path, "correct")
    incorrect_folder = os.path.join(directory_path, "incorrect")

    if not os.path.exists(correct_folder):
        os.makedirs(correct_folder)
    if not os.path.exists(incorrect_folder):
        os.makedirs(incorrect_folder)

def read_paths(file):
    global firmware_image_file_paths
    firmware_image_file_paths = set()
    with open(file, "r") as fp:
        for line in fp:
            firmware_image_file_paths.add(line.strip())
    # print(firmware_image_file_paths)

def all_firmware_image_paths(json_file_path):
    global file_paths
    file_paths = set()
    with open(json_file_path, "r") as fp:
        data = json.load(fp)
        for k, v in data.items():
            file_paths.add(v)


def move_files(firmware_image_file_paths, file_paths):
    for path in file_paths:
        if path in firmware_image_file_paths:
            os.system("cp %s %s" % (path, correct_folder))
        else:
            os.system("cp %s %s" % (path, incorrect_folder))

create_folders(args.directory)
read_paths(args.path)
all_firmware_image_paths(args.file)
move_files(firmware_image_file_paths, file_paths)

