import os
import json
from dotenv import load_dotenv

load_dotenv()
file_path = os.getenv("file_path")
json_file = open(file_path + "/links.json")
link_dict = json.load(json_file)
max = len(link_dict)

file_path = str(file_path)
file_path = file_path.replace(" ", "\ ")
command = "#!/usr/bin/env bash\n"

for i in range(1, max + 1):
    command = command + "python3 " + file_path + "/Classroom\ Notifier.py " + str(i) + " &"
    
    if i != max:
        command = command + "\n"

with open ('run.sh', 'w') as sh:
	sh.write(command)