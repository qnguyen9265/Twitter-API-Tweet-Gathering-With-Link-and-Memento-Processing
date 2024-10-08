# process-urls.py

import requests 
import re

INPUT_FILE = "expanded-urls.jsonl"
OUTPUT_FILE = "final-uris.jsonl"

# websites to not save links from
excludes = re.compile("twitter\.com|youtube\.com|twitch\.tv|oundcloud\.com|imgur\.com")

# gets all URIs already in OUTPUT_FILE
seen = set()
with open(OUTPUT_FILE, 'r') as output:
    for uri in output:
        seen.add(uri)
    
with open(INPUT_FILE, 'r') as expanded_urls:
    uri = ""
    for url in expanded_urls:
        if(excludes.search(url) != None):
                continue
        try:
            r = requests.get(url, timeout = 5, allow_redirects=True)
        except:
            print("Error with link.")
        print(r)
        print ("   " + r.url)
        
        if r.status_code == 200:
            # website links that are likely to only have video/audio are not saved
            if(excludes.search(r.url) != None):
                print("   Website excluded from being saved.")
                continue

            # If the website url is unique, it gets saved in OUTPUT_FILE as a new line
            with open(OUTPUT_FILE, 'a') as output:
                if (r.url+'\n') not in seen:
                    print("   Link saved.")
                    output.write('%s\n' % r.url)
                    seen.add((r.url+'\n'))
                else:
                    print("   Link already seen.")
                    
#with open(OUTPUT_FILE, 'a') as output:
#    for link in seen:
#        output.write('%s\n' % link)