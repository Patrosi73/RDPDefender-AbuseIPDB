import json
import time
import os
import requests
from datetime import datetime, timezone
import pytz
with open("keys.json") as keys_data:
    keys = json.load(keys_data)
apikey = keys['apikey']
path = keys['blocklist']
processed_lines_file = 'processed_lines.txt'


def get_last_entry(db_file):
    with open(db_file, "r") as f:
        return f.readlines()[-1].strip()
    
def extract_info(line):
    parts = line.split(',')
    ip_address = parts[0].strip()
    timestamp = parts[1].strip()
    return ip_address, timestamp

def report(ip_address, timestamp):
    system_timezone = str(datetime.now(pytz.timezone('UTC')).astimezone().tzinfo)
    
    timestamp_utc = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").replace(tzinfo=pytz.timezone(system_timezone)).astimezone(timezone.utc)
    timestamp_utc_str = timestamp_utc.strftime("%Y-%m-%dT%H:%M:%SZ")


    endpoint = 'https://api.abuseipdb.com/api/v2/report'
    payload = {
        'ip': ip_address,
        'categories': '14,18',
        'comment': 'RDP Brute-Forcing',
        'timestamp': timestamp_utc_str
    }
    headers = {
        'Key': apikey,
        'Accept': 'application/json'
    }
    response = requests.post(endpoint, data=payload, headers=headers)
    print("API Response:", response.text)

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
                report(ip_address, timestamp)
                processedfile.write(ip_address + ',' + timestamp + '\n')
                time.sleep(5)

report_missing(path, processed_lines_file)

while True:
    with open(processed_lines_file, 'a+') as file:
        file.seek(0)
        last_entry = get_last_entry(path)
        if last_entry not in file.read():
            ip_address, timestamp = extract_info(last_entry)
            print("Reporting IP: " + ip_address + ", Date: " + timestamp)
            report(ip_address, timestamp)
            file.write(ip_address + ',' + timestamp + '\n')
            file.seek(0)

    time.sleep(5)
