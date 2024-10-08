import subprocess
import sys
import json

INPUT_FILE = "final-uris.jsonl"

with open(INPUT_FILE, 'r') as final_uris:
    i = 0
    for uri in final_uris:
        i += 1
        if i > 1071:
            break
        
        uri = uri.rstrip()
        cmd = ('C:\memgator\memgator -k 3 -F 1 -f JSON "{}"'.format(uri))
        
        print ("Currently on: {}".format(i)) 
        print("   " + cmd)
        
        output = open("timemaps/{}.json".format(i), "w")
        timemap = subprocess.run(["powershell.exe", "-Command", cmd], stdout = output, stderr = sys.stderr)
        output.close()