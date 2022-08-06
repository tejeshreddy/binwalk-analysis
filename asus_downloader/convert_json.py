import json
import re

complete_data = {}
counter = 0
visited = set()

with open("asus-metadata-1.txt") as fp:
    for line in fp:
        data = json.loads(line)

        for k, v in data.items():
            k = re.sub('[^0-9a-zA-Z/.]+', '_', k)
            if k not in visited:
                complete_data[counter] = {"key": k, "value": v}
                visited.add(k)
                counter += 1

with open("asus_metadata.json", "w") as fp:
    fp.write(json.dumps(complete_data, indent=2))

