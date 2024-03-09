import requests
import os
import time
import json

with open("keys.json") as keys_data:
    keys = json.load(keys_data)
apikey = keys['apikey']
path = keys['logfile']
target_text = 'Service - Blocking address'


def get_last_line(logfile):
    with open(logfile, "r") as f:
        last_line = f.readlines()[-1]
    return last_line.strip()

while True:
    last_line = get_last_line(path)
    print("Last log: " + last_line)
    if target_text in last_line:
        print("Found")
    time.sleep(1)
