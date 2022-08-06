import json
import os
import wget
from urllib.request import Request, urlopen
import requests
import shutil

# job_completion_index = os.getenv('JOB_COMPLETION_INDEX')
download_folder = "/shared/firmware-images/asus"

with open("asus_metadata.json") as fp:
    metadata = json.load(fp)

for index in metadata:
    with open("completion_index.txt", "a") as fp:
        fp.write(index)
        fp.write("\n")
    
    if "bios" not in metadata[index]["key"]:
        r = requests.get(metadata[index]["value"], stream=True)
        if r.status_code == 200:
            with open(metadata[index]["key"], 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

