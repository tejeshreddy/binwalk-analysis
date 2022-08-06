"""
Commands:

dlink: python3 path_file_generator.py -p /tank/kubernetes/firmware-images/dlink -c dlink
tenda: python3 path_file_generator.py -p /shared/firmware-images/tenda -c tenda
dlink-legacy: python3 path_file_generator.py -p /shared/firmware-images/dlink/dlink-legacy -c dlink_legacy
netgear: python3 path_file_generator.py -p /shared/firmware-images/netgear -c netgear
tplink: python3 path_file_generator.py -p /shared/firmware-images/tplink -c tplink
trendnet: python3 path_file_generator.py -p /shared/firmware-images/trendnet -c trendnet
asus: python3 path_file_generator.py -p /shared/firmware-images/asus -c asus
"""
import argparse
import os
import subprocess
import re
import logging
import json


exclusion_extenstions = ["pdf"]
binwalk_folder = "/shared/firmware-images/binwalk-result"

parser = argparse.ArgumentParser(description='Enter the path for the file directory')
parser.add_argument("-p", "--path", help = "Please enter the path of the directory")
parser.add_argument("-c", "--customer", help = "Please enter the name of the customer you're processing")

args = parser.parse_args()

def list_zip_files(path):
    zip_files = []
    files = os.listdir(path)
    files = [path + "/" + file for file in files]

    for file in files:
        if (file.rsplit(".")[-1]).lower() not in exclusion_extenstions:
            zip_files.append(file)
    return zip_files

files = list_zip_files(args.path)
hmap = {}


for key, file_path in enumerate(files):
    hmap[key] = file_path

with open(os.path.join(binwalk_folder, args.customer + ".json"), "w") as fp:
    json.dump(hmap, fp)

