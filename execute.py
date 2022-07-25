import os
import json
from dotenv import load_dotenv
from sys import platform

load_dotenv()
file_path = os.getenv("file_path")
json_file = open(file_path + "/links.json")
link_dict = json.load(json_file)
max = len(link_dict)

file_path = str(file_path)
file_path = file_path.replace(" ", "\ ")

if platform == "linux" or platform == "darwin":
    if platform == "linux": # Linux
        command = "#!/bin/bash"

    elif platform == "darwin": # Mac OS
        command = "#!/usr/bin/env bash"

    for i in range(1, max + 1):
        command = command + "\npython3 " + file_path + "/Classroom\ Notifier.py " + str(i) + " &"

    with open ('run.sh', 'w') as sh:
        sh.write(command)

elif platform == "win32": # Windows
    print("Windows is not supported yet. We will update the code soon.")
