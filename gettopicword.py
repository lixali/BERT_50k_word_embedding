Profession = ["teacher,author,mechanic,broker,baker,surveyor,laborer,surgeon,gardener,painter,dentist,janitor,athlete,manager,conductor,carpenter,housekeeper,secretary,economist,geologist,clerk,doctor,judge,physician,lawyer,artist,instructor,dancer,photographer,inspector,musician,soldier,librarian,professor,psychologist,nurse,sailor,accountant,architect,chemist,administrator,physicist,scientist,farmer".split(",")]

Personality_Traits = ["adventurous,helpful,affable,humble,capable,imaginative,charming,impartial,confident,independent,conscientious,keen,cultured,meticulous,dependable,observant,discreet,optimistic,persistent,encouraging,precise,exuberant,reliable,fair,trusting,fearless,valiant,gregarious,arrogant,rude,sarcastic,cowardly,dishonest,sneaky,stingy,impulsive,sullen,lazy,surly,malicious,obnoxious,unfriendly,picky,unruly,pompous,vulgar".split(",")]

Extremism = ["terror,terrorism,violence,attack,death,military,war,radical,injuries,bomb,target,,conflict,dangerous,kill,murder,strike,dead,violence,fight,death,force,stronghold,wreckage,aggression,,slaughter,execute,overthrow,casualties,massacre,retaliation,proliferation,militia,hostility,debris,acid,,execution,militant,rocket,guerrilla,sacrifice,enemy,soldier,terrorist,missile,hostile,revolution,resistance,shoot".split(",")]

Physical_Appearance = ["alluring,voluptuous,blushing,homely,plump,sensual,gorgeous,slim,bald,athletic,fashionable,stout,ugly,muscular,slender,feeble,handsome,healthy,attractive,fat,weak,thin,pretty,beautiful,strong".split(",")]


Profession = [word for sublist in Profession for word in sublist ]
Personality_Traits = [word for sublist in Personality_Traits for word in sublist ]
Extremism = [word for sublist in Extremism for word in sublist ]
Physical_Appearance = [word for sublist in Physical_Appearance for word in sublist ]

# print(gender_bias)
# print(race_bias)
# print(religion_bias)
# print(age_bias)
# print(eco_bias)


all_words = Profession + Personality_Traits + Extremism + Physical_Appearance
print(len(all_words))
#quit()

import json
import re

import glob
from collections import defaultdict
#f = "/mnt/c/Users/charl/Downloads/saved_json_test/*.json"
f = "./saved_json_randomPicked/*.json"
confile = "./containfiletopic.json"
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
        #print(topic)
        #print(file)
        with open(file,"r",encoding='utf-8') as currfile:
            for line in currfile.readlines():
                #print(line)
                if '"text":' in line:
                    a,b = line.split(":",1)
                    b_l = re.split(" |,|\\.",b)
                    if topic in b_l: 
                        fileThatContains[topic] = [file]
                        foundword[topic] = True
                        # with open(confile,"a",encoding='utf-8') as containfile: 
                        #     fileThatContains_object = json.dumps({topic: file},indent=4)
                        #     containfile.write(fileThatContains_object)


                        break

def writeToJson(fileThatContains):

    with open(confile,"w",encoding='utf-8') as containfile: 
        fileThatContains_object = json.dumps(fileThatContains,indent=4)
        containfile.write(fileThatContains_object)        

writeToJson(fileThatContains)                        

print(len(fileThatContains))

#quit()