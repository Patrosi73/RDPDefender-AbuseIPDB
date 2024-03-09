import json
import time

with open("keys.json") as keys_data:
    keys = json.load(keys_data)
apikey = keys['apikey']
path = keys['logfile']
target_text = 'Service - Blocking address'
processed_lines_file = 'processed_lines.txt'

def get_last_line(logfile):
    with open(logfile, "r") as f:
        return f.readlines()[-1].strip()


while True:
    with open(processed_lines_file, 'a') as file:
        last_line = get_last_line(path)

        if last_line not in file.read():
            print("Last log: " + last_line)

            if target_text in last_line:
                print("Found")

            file.write(last_line + '\n')

    time.sleep(1)
