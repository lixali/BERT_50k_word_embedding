gender_bias = ["he,son,his,him,father,man,boy,himself,male,brother,sons,fathers,men,boys,males,brothers,uncle,uncles,nephew,nephews".split(","),
               "she,daughter,hers,her,mother,woman,girl,herself,female,sister,daughters,mothers,women,girls,femen,sisters,aunt,aunts,niece,nieces".split(",")]
#eco_bias = [("rich","wealthy"),("poor","impoverished")]
#race_bias = ["black,blacks,Black,Blacks,African,Afro,Alonzo,Jamel,Lerone,Percell,Theo,Alphonse,Jerome,Leroy,Rasaan,Torrance,Darnell,Lamar,Lionel,Rashaun,Tvree,Deion,Lamont,Malik,Terrence,Tyrone,Everol,Lavon,Marcellus,Terryl,Wardell,Aiesha,Lashelle,Nichelle,Shereen,Temeka,Ebony,Latisha,Shaniqua,Tameisha,Teretha,Jasmine,Latonya,Shanise,Tanisha,Tia,Lakisha,Latoya,Sharise,Tashika,Yolanda,Lashandra,Malika,Shavonn,Tawanda,Yvette".split(","),
#             "white,whites,White,Whites,Caucasian,European,Anglo,Adam,Chip,Harry,Josh,Roger,Alan,Frank,Ian,Justin,Ryan,Andrew,Fred,Jack,Matthew,Stephen,Brad,Greg,Jed,Paul,Todd,Brandon,Hank,Jonathan,Peter,Wilbur,Amanda,Courtney,Heather,Melanie,Sara,Amber,Crystal,Katie,Meredith,Shannon,Betsy,Donna,Kristin,Nancy,Stephanie,Bobbie-Sue,Ellen,Lauren,Peggy,Sue-Ellen,Colleen,Emily,Megan,Rachel,Wendy".split(",")]

race_bias = ["black,blacks,Black,Blacks,African,african,Afro".split(","),
             "white,whites,White,Whites,Caucasian,caucasian,European,european,Anglo".split(",")]

religion_bias = ["baptism,messiah,catholicism,resurrection,christianity,salvation,protestant,gospel,trinity,jesus,christ,christian,cross,catholic,church".split(","),
                "allah,ramadan,turban,emir,salaam,sunni,koran,imam,sultan,prophet,veil,ayatollah,shiite,mosque,islam,sheik,muslim,muhammad".split(",")]

#sentiment_bias = ["caress,freedom,health,love,peace,cheer,friend,heaven,loyal,pleasure,diamond,gentle,honest,lucky,rainbow,diploma,gift,honor,miracle,sunrise,family,happy,laughter,paradise,vacation".split(","),
#                 "abuse,crash,filth,murder,sickness,accident,death,grief,poison,stink,assault,disaster,hatred,pollute,tragedy,divorce,jail,poverty,ugly,cancer,kill,rotten,vomit,agony,prison".split(",")]

age_bias = ["Taylor,Jamie,Daniel,Aubrey,Alison,Miranda,Jacob,Arthur,Aaron,Ethan".split(","),
           "Ruth,William,Horace,Mary,Susie,Amy,John,Henry,Edward,Elizabeth".split(",")]

eco_bias = ["rich,richer,richest,affluence,advantaged,wealthy,costly,exorbitant,expensive,exquisite,extravagant,flush,invaluable,lavish,luxuriant,luxurious,luxury,moneyed,opulent,plush,precious,priceless,privileged,prosperous,classy".split(","),
           "poor,poorer,poorest,poverty,destitude,needy,impoverished,economical,inexpensive,ruined,cheap,penurious,underprivileged,penniless,valueless,penury,indigence,bankrupt,beggarly,moneyless,insolvent".split(",")]

gender_bias = [word for sublist in gender_bias for word in sublist ]
race_bias = [word for sublist in race_bias for word in sublist ]
religion_bias = [word for sublist in religion_bias for word in sublist ]
age_bias = [word for sublist in age_bias for word in sublist ]
eco_bias = [word for sublist in eco_bias for word in sublist ]

# print(gender_bias)
# print(race_bias)
# print(religion_bias)
# print(age_bias)
# print(eco_bias)


all_words = gender_bias + race_bias + religion_bias + age_bias + eco_bias
print(len(all_words))


import json
import re

import glob
from collections import defaultdict
#f = "/mnt/c/Users/charl/Downloads/saved_json_test/*.json"
f = "./saved_json_randomPicked/*.json"
confile = "./containfilebias.json"
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