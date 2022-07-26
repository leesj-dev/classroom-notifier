import os
import yaml
from dotenv import load_dotenv
from sys import platform

load_dotenv()
file_path = os.getenv("file_path")
command = ""

def getMax(file_path, slash):
    yaml_file = open(file_path + slash + "src" + slash + "config.yaml")
    link_dict = yaml.safe_load(yaml_file)
    max = len(link_dict)

    return max

if platform == "linux" or platform == "darwin":
    slash = "/"
    max = getMax(file_path, slash)
    file_path_str = str(file_path)
    file_path_str = file_path.replace(" ", "\ ")

    if platform == "linux":  # Linux
        command = "#!/bin/bash"

    elif platform == "darwin":  # Mac OS
        command = "#!/usr/bin/env bash"

    for i in range(1, max + 1):
        command = command + "\npython3 " + file_path_str + "/src/main.py " + str(i) + " &"

    with open (file_path + slash + "src" + slash + 'run.sh', 'w') as sh:
        sh.write(command)

elif platform == "win32":  # Windows
    slash = "\\"
    max = getMax(file_path, slash)
    file_path_str = str(file_path)
    command = ""

    for i in range(1, max + 1):
        command = command + 'start python3 "' + file_path_str + '\src\main.py ' + str(i) + '"'
        if i != max:
            command = command + "\n"

    with open (file_path + slash + "src" + slash + 'run.bat', 'w') as bat:
        bat.write(command)
