import sys
import json
import re
from datetime import datetime
from datetime import date
from datetime import timedelta
import matplotlib.pyplot as plt

# number of momentos, number of URIs with that number of mementos
memento_uris = [[0, 0]]
mementos = 0
# list of earliest dates
earliest_datetimes = []
earliest = ""

longest = []
LONGEST_THRESHOLD = 1000

# regex to check up to before the T in the datetime string
no_time = re.compile("^[0-9]{4}-[0-9]{2}-[0-9]{2}")

for i in range(1, 1072):
    #if i > 9:
    #    break
    
    with open("timemaps/{}.json".format(i), 'r') as timemap:
        data = None
        print("Currently on: {}".format(i))
        try:
            data = json.load(timemap)
        except:
            print("     No timemap found.")
            memento_uris[0][1] += 1 # the 0 memento value is always at [0][]
            continue
        
        if data != None:
            #formatted_data = json.dumps(data, indent=2)
            #print(formatted_data)
            
            mementos = len(data['mementos']['list'])
            print("     Number of mementos: {}".format(mementos))
            
            found = False
            for j in range(len(memento_uris)):
                check = memento_uris[j][0]
                if check == mementos:
                    memento_uris[j][1] += 1
                    found = True
            if found == False:
                memento_uris.append([mementos, 1])
            
            earliest = data['mementos']['first']['datetime']
            m = no_time.match(earliest)
            earliest_datetimes.append([i, m.group(0), mementos]) # all of the information for question 4
            print("     Datetime of earliest memento: " + earliest)
            
            if mementos > LONGEST_THRESHOLD:
                longest.append([mementos, data['original_uri']])

# sort and print results
print("\nFinal output:")
memento_uris.sort()
print("Memento number and URIs: \n{}".format(memento_uris))
earliest_datetimes.sort(key = lambda x: x[1])
print("\nFile number and earliest datetime: \n{}".format(earliest_datetimes))
longest.sort()
print("\nURIs with more than {} mementos: \n{}".format(LONGEST_THRESHOLD, longest))

dates = []
mems = []
age = []
numRecent = 0
now = datetime.strftime(date.today(), '%Y-%m-%d')
#print(type(now))
now = datetime.strptime(now, "%Y-%m-%d").date()
#print(now)
#print(type(now))
for i in range(len(earliest_datetimes)):
    dates.append(datetime.strptime(earliest_datetimes[i][1], "%Y-%m-%d").date())
    mems.append(earliest_datetimes[i][2])
    temp = now - dates[i]
    temp = (timedelta.total_seconds(temp) / 86400)
    age.append(temp)
    if temp < 7:
        numRecent += 1

print("\nNumber of recent mementos: {}".format(numRecent))
plt.scatter(age, mems)
plt.suptitle("URI-R Age vs. Memento Quantity")
plt.xlabel("Age in Days")
plt.ylabel("Number of Mementos")
plt.savefig("Q4-scatterplot.png")
plt.show()