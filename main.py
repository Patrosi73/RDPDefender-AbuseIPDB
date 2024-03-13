import json
import time
import os
import requests
from datetime import datetime, timezone, timedelta

with open("keys.json") as keys_data:
    keys = json.load(keys_data)
apikey = keys['apikey']
path = keys['blocklist']
processed_lines_file = 'processed_lines.txt'

def get_last_entry(db_file):
    with open(db_file, "r") as f:
        lines = f.readlines()
        return lines[-1].strip() if lines else None

def extract_info(line):
    parts = line.split(',')
    return parts[0].strip(), parts[1].strip()

def report(ip_address, timestamp):
    local_tz = timezone(timedelta(seconds=-time.timezone))
    local_dt = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p").replace(tzinfo=local_tz)
    timestamp_utc = local_dt.astimezone(timezone.utc)
    timestamp_utc_str = timestamp_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    endpoint = 'https://api.abuseipdb.com/api/v2/report'
    payload = {
        'ip': ip_address,
        'categories': '14,18',
        'comment': 'RDP Brute-Forcing',
        'timestamp': timestamp_utc_str
    }
    headers = {'Key': apikey, 'Accept': 'application/json'}
    response = requests.post(endpoint, data=payload, headers=headers)
    print("API Response:", response.text)

def report_missing(blocklistfile, processed_file):
    with open(blocklistfile, "r") as blacklist, open(processed_file, 'a+') as processedfile:
        for line in blacklist:
            line = line.strip()
            processedfile.seek(0)
            if line not in processedfile.read():
                ip_address, timestamp = extract_info(line)
                print("Reporting IP:", ip_address)
                report(ip_address, timestamp)
                processedfile.write(f"{ip_address},{timestamp}\n")
                time.sleep(5)

report_missing(path, processed_lines_file)

while True:
    with open(path, "r") as file, open(processed_lines_file, 'a+') as processedfile:
        processedfile.seek(0)
        last_entry = get_last_entry(path)

        if last_entry is not None and last_entry not in processedfile.read():
            ip_address, timestamp = extract_info(last_entry)
            print("Reporting IP:", ip_address)
            report(ip_address, timestamp)
            processedfile.write(f"{ip_address},{timestamp}\n")
            processedfile.seek(0)

    time.sleep(5)
