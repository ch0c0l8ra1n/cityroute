import sys
import subprocess
import requests
import re
import os

if len(sys.argv) < 2:
    print("Usage: python3 cityroute.py host")
    exit()

if "TOKEN" not in os.environ:
    print("Set TOKEN to your token from https://ipinfo.io")
    exit()

host = sys.argv[1]
token = os.environ["TOKEN"]
traceroute = subprocess.Popen(["traceroute",host],stdout=subprocess.PIPE)

hops = []

def get_location(ip):
    url = f"https://ipinfo.io/{ip}/json?token={token}"
    resp = requests.get(url)
    return resp.json()

i = 0
while True:
    i+=1
    line_raw = traceroute.stdout.readline()
    if not line_raw:
        break
    
    line = line_raw.decode().strip("\n")
    #print(repr(line))

    match = re.match(r" \d+  (?:\* )*[\w\-\.]+ *\((.*?)\)",line)
    
    
    if match:
        ip, = match.groups()
        hops.append(ip)
        location = get_location(ip)

        if "error" in location:
            print(f"{i} {location},{ip}")
        if "bogon" in location:
            print(f"{i} {ip: <16} {'LOCAL':>82}")
        else:
            print(f"{i} {ip: <16} {location['org'] : >60} {location['city'] : >20}")
    
    elif "* * *" in line:
        print(f"{i} TIMEOUT")




