# Firmware Parallel

## Steps to Run

1. Run the path_file_generator.py to get the list of all the zip files to a json file
Command to Run

```bash
python3 path_file_generator.py -p /tank/kubernetes/firmware-images/validset/dlink_latest -c dlink
```

2. Change the docker file command to be run to match the new customer. Note, use the same customer name as used to generate the JSON file.

3. Change the following in `parallel-deployment.yaml` file.
    - Total number of images
    - The docker image that has to be pulled





## Bash Commands

```bash

docker build -t tejeshreddy/binwalk:v1 .
docker image push tejeshreddy/binwalk:v1
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalk:v1 --push .


docker build -t tejeshreddy/service:v1 .
docker image push tejeshreddy/service:v1
docker buildx build --platform linux/amd64 -t tejeshreddy/service:v1 --push .


docker build -t tejeshreddy/binwalkparallel:dlink .
docker image push tejeshreddy/binwalkparallel:dlink
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:dlink --push .


docker build -t tejeshreddy/binwalkparallel:tenda .
docker image push tejeshreddy/binwalkparallel:tenda
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:tenda --push .

docker build -t tejeshreddy/binwalkparallel:netgear .
docker image push tejeshreddy/binwalkparallel:netgear
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:netgear --push .

docker build -t tejeshreddy/binwalkparallel:tplink .
docker image push tejeshreddy/binwalkparallel:tplink
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:tplink --push .

docker build -t tejeshreddy/binwalkparallel:trendnet .
docker image push tejeshreddy/binwalkparallel:trendnet
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:trendnet --push .

docker build -t tejeshreddy/binwalkparallel:asus .
docker image push tejeshreddy/binwalkparallel:asus
docker buildx build --platform linux/amd64 -t tejeshreddy/binwalkparallel:asus --push .

```


Renaming the files
```python
import re
import os

for filename in os.listdir("."):
    os.rename(filename, re.sub('[^0-9a-zA-Z/.]+', '_', filename))
```
