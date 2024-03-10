import json
import time
import os
import requests

with open("keys.json") as keys_data:
    keys = json.load(keys_data)
apikey = keys['apikey']
path = keys['blocklist']
target_text = 'Service - Blocking address'
processed_lines_file = 'processed_lines.txt'


def get_last_entry(db_file):
    with open(db_file, "r") as f:
        return f.readlines()[-1].strip()
    
def extract_info(line):
    parts = line.split(',')
    ip_address = parts[0].strip()
    timestamp = parts[1].strip()
    return ip_address, timestamp

def report_missing(blocklistfile, processed_file):
    with open(blocklistfile, "r") as blacklist:
        blocklist_content = blacklist.readlines()

    with open(processed_file, 'a+') as processedfile:
        for line in blocklist_content:
            line = line.strip()
            processedfile.seek(0)
            if line not in processedfile.read():
                ip_address, timestamp = extract_info(line)
                print("Reporting IP: " + ip_address)
                processedfile.write(ip_address + ',' + timestamp + '\n')
                time.sleep(1)

report_missing(path, processed_lines_file)

while True:
    with open(processed_lines_file, 'a+') as file:
        file.seek(0)
        last_entry = get_last_entry(path)
        if last_entry not in file.read():
            ip_address, timestamp = extract_info(last_entry)
            print("Reporting IP: " + ip_address + ", Date: " + timestamp)
            file.write(ip_address + ',' + timestamp + '\n')
            file.seek(0)

    time.sleep(1)
