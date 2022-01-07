import os
import sys
import socket
import platform
import json
serving_type = input("1-local server\n2-local network\n->")
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
print(f"ip: {s.getsockname()[0]}")
print(f"os: {platform.system()}")
ip_addres = s.getsockname()[0]
s.close()
the_edited = f"""# Host addresses
127.0.0.1  localhost
127.0.1.1  marshall
{ip_addres}  {ip_addres}
::1        localhost ip6-localhost ip6-loopback
ff02::1    ip6-allnodes
ff02::2    ip6-allrouters
    """
try:
    with open("/etc/hosts" , "w") as hosts_set:
        hosts_set.write(the_edited)
except PermissionError:
    print("run the script as root")
    exit()

if os.path.exists("settings.json") != True:
    open("settings.json" , "w").write("{}")
try:
    json.loads("settings.json").read()
except json.decoder.JSONDecodeError:
    open("settings.json" , "w").write("{}")
with open("settings.json") as settings_file:
    acv = json.loads(settings_file.read())
    acv["settings"] = {}
    acv["settings"]["ip_addres"] = ip_addres
    acv["settings"]["serving_type"] = serving_type
    open("settings.json" , "w").write(json.dumps(acv))
