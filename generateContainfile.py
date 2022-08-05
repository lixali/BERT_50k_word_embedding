#!/usr/bin/env python
# coding: utf-8

import csv

with open('50k_word.csv', newline='') as f:
    reader = csv.reader(f)
    all_words = list(reader)
    all_words = [item for sublist in all_words for item in sublist]



print(len(all_words))
#print(len(all_words))
#quit()
import json
import re

import glob
from collections import defaultdict
#f = "/mnt/c/Users/charl/Downloads/saved_json_test/*.json"
f = "./saved_json_randomPicked/*.json"
confile = "./containfile.json"
count = 0
articles = {}
hashnumber = 0
articles2 = defaultdict(list)
foundarticleshash = []
fileThatContains = defaultdict(list)
foundword = defaultdict(lambda: False)


for file in glob.glob(f):

    for topic in all_words:

        if foundword[topic]: continue
        #print(file)
        with open(file,"r",encoding='utf-8') as currfile:
            for line in currfile.readlines():
                #print(line)
                if '"text":' in line:
                    a, b = line.split(":", 1)
                    b_l = re.split(" |,|\\.",b)
                    currentCount = b_l.count(topic)
                    if currentCount > 0: 
                        fileThatContains[topic] = [file]
                        foundword[topic] = True
                        break

top50Articles = defaultdict(list)
def writeToJson(fileThatContains):

    with open(confile,"w",encoding='utf-8') as containfile: 
        fileThatContains_object = json.dumps(fileThatContains, indent=4)
        containfile.write(fileThatContains_object)        



writeToJson(fileThatContains)    
print(len(fileThatContains))                    
#quit()

