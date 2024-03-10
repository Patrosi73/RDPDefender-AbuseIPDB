# RDPDefender-AbuseIPDB
A simple tool to automatically report all blocked IPs with RDP Defender to AbuseIPDB.

# Installation
- If you haven't already, download Python and install the requests package with pip:
```
pip install requests
```
- Git clone this repository/download it as a zip, then extract it
- Create a file called `keys.json` with the following content:

```
{
    "blocklist" : "C:\\Program Files (x86)\\RDP Defender\\blocked.dat",
    "apikey" : "YOUR_KEY_HERE"
}
```

with YOUR_KEY_HERE being your AbuseIPDB API key.

- Create an empty file called `processed_lines.txt` - this will store reported IPs so when you re-run the tool it won't report them again.

Run main.py and it'll start reporting them!
