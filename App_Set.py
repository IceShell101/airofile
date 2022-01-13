import os
import sys
import platform
import json
serving_type = input("1-local server\n2-local network\n->")
print(f"ip: ")
print(f"os: {platform.system()}")
ip_addres = "test"

if os.path.exists("settings.json") != True:
    open("settings.json" , "w").write("{}")
try:
    json.loads("settings.json").read()
except json.decoder.JSONDecodeError:
    open("settings.json" , "w").write("{}")
with open("settings.json") as settings_file:
    acv = json.loads(settings_file.read())
    acv["settings"] = {}
    acv["settings"]["serving_type"] = serving_type
    open("settings.json" , "w").write(json.dumps(acv))
