import csv
import os
import json
import hashlib
import time

# CHIP007 json template 
print("Setting CHIP-007 format...")
time.sleep(0.5)
json_obj = {
    "format": "CHIP-0007",
    "name": None,
    "description": None,
    "minting_tool": None,
    "sensitive_content": False,
    "series_number": None,
    "series_total": 20,
    "attributes": [
        {
            "trait_type": "gender",
            "value": None
        }
    ],
    "collection": {
        "name": "Zuri NFT Tickets for Free Lunch",
        "id": "b774f676-c1d5-422e-beed-00ef5510c64d",
        "attributes": [
            {
                "type": "description",
                "value": "Rewards for accomplishments during HNGi9."
            }
        ]
    }
}

# a dictionary that will contain the string equivalents of all JSONs that will be generated
json_dict = {}


# define file path. will be used later.
print("Defining file path...")
time.sleep(0.5)
script_dir = os.path.dirname(__file__)
print(script_dir)

# parse csv content to create JSON file for each row. store in local folder. 
print('creating CHIP-007 JSON formats...')
time.sleep(0.5)
with open(script_dir + "/dcsv.csv", 'r') as csv_file:
    for row in csv.reader(csv_file):
        json_now = json_obj
        if not row[0]:
            pass
        if row[0] == "":
            pass
        if 'Series' in (row[0])[0:6]:
            pass
        if (row[0])[0:4] == 'TEAM':
            json_now['minting_tool'] = row[0]
            pass
        else:
            json_now['series_number'] = row[0]
            json_now['name'] = row[2]
            json_now['description'] = row[3]
            (json_now['attributes'][0])['value'] = row[4]

            script_dir = os.path.dirname(__file__)
            rel_file_path = "/json_files/" + row[1] + ".json"
            abs_file_path = os.path.join(script_dir, rel_file_path)
            with open(script_dir + rel_file_path, "w") as new_file:
                json.dump(json_now, new_file)
            
            #add series number, json as key, value in dictionary
            key = row[0]
            json_dict[key] = json.dumps(json_now)


# encode each json in json_dict to SHA256 format, update value in json_dict. store the hexadecimal equivalent of sha256.
print("Encoding json to SHA256")
time.sleep(0.5)
for key, value in json_dict.items():
    encoded_value = hashlib.sha256(value.encode())
    json_dict[key] = encoded_value.hexdigest()


# add new column "SHA" to new csv file. 
print("writing to new output.csv...")
time.sleep(0.5)
all_new_rows = []

old = open(os.path.join(script_dir, "dcsv.csv"))
read = csv.reader(old)
headers = next(read)
headers.append("SHA256")

all_new_rows.append(headers)

for row in read:
    sha = json_dict.get(row[0])
    if sha == None:
        pass
    else:
        row.append(sha)
        all_new_rows.append(row)  

new_path = os.path.join(script_dir, "output.csv")

new_file2 = open(new_path, 'w+', newline = '')

with new_file2:
    write = csv.writer(new_file2)
    write.writerows(all_new_rows)

print("Done.")