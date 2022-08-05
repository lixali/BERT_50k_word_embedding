import subprocess
import json
from collections import defaultdict
f = open ('embedding4.json', "r")
embedding = json.loads(f.read())

f2 = open ('vector.txt', "a")

for word in embedding:
    curr = str(word) + " "
    for number in embedding[word]:
        curr = curr + str(number) + " "
    
    
    f2.write(curr)
    f2.write("\n")

f.close()
f2.close()