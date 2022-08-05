Profession = ["teacher,author,mechanic,broker,baker,surveyor,laborer,surgeon,gardener,painter,dentist,janitor,athlete,manager,conductor,carpenter,housekeeper,secretary,economist,geologist,clerk,doctor,judge,physician,lawyer,artist,instructor,dancer,photographer,inspector,musician,soldier,librarian,professor,psychologist,nurse,sailor,accountant,architect,chemist,administrator,physicist,scientist,farmer".split(",")]

Personality_Traits = ["adventurous,helpful,affable,humble,capable,imaginative,charming,impartial,confident,independent,conscientious,keen,cultured,meticulous,dependable,observant,discreet,optimistic,persistent,encouraging,precise,exuberant,reliable,fair,trusting,fearless,valiant,gregarious,arrogant,rude,sarcastic,cowardly,dishonest,sneaky,stingy,impulsive,sullen,lazy,surly,malicious,obnoxious,unfriendly,picky,unruly,pompous,vulgar".split(",")]

Extremism = ["terror,terrorism,violence,attack,death,military,war,radical,injuries,bomb,target,,conflict,dangerous,kill,murder,strike,dead,violence,fight,death,force,stronghold,wreckage,aggression,,slaughter,execute,overthrow,casualties,massacre,retaliation,proliferation,militia,hostility,debris,acid,,execution,militant,rocket,guerrilla,sacrifice,enemy,soldier,terrorist,missile,hostile,revolution,resistance,shoot".split(",")]

Physical_Appearance = ["alluring,voluptuous,blushing,homely,plump,sensual,gorgeous,slim,bald,athletic,fashionable,stout,ugly,muscular,slender,feeble,handsome,healthy,attractive,fat,weak,thin,pretty,beautiful,strong".split(",")]

Profession = [word for sublist in Profession for word in sublist ]
Personality_Traits = [word for sublist in Personality_Traits for word in sublist ]
Extremism = [word for sublist in Extremism for word in sublist ]
Physical_Appearance = [word for sublist in Physical_Appearance for word in sublist ]

all_words = Profession + Personality_Traits + Extremism + Physical_Appearance

gender_bias = ["he,son,his,him,father,man,boy,himself,male,brother,sons,fathers,men,boys,males,brothers,uncle,uncles,nephew,nephews".split(","),
               "she,daughter,hers,her,mother,woman,girl,herself,female,sister,daughters,mothers,women,girls,femen,sisters,aunt,aunts,niece,nieces".split(",")]
#eco_bias = [("rich","wealthy"),("poor","impoverished")]
#race_bias = ["black,blacks,Black,Blacks,African,Afro,Alonzo,Jamel,Lerone,Percell,Theo,Alphonse,Jerome,Leroy,Rasaan,Torrance,Darnell,Lamar,Lionel,Rashaun,Tvree,Deion,Lamont,Malik,Terrence,Tyrone,Everol,Lavon,Marcellus,Terryl,Wardell,Aiesha,Lashelle,Nichelle,Shereen,Temeka,Ebony,Latisha,Shaniqua,Tameisha,Teretha,Jasmine,Latonya,Shanise,Tanisha,Tia,Lakisha,Latoya,Sharise,Tashika,Yolanda,Lashandra,Malika,Shavonn,Tawanda,Yvette".split(","),
#             "white,whites,White,Whites,Caucasian,European,Anglo,Adam,Chip,Harry,Josh,Roger,Alan,Frank,Ian,Justin,Ryan,Andrew,Fred,Jack,Matthew,Stephen,Brad,Greg,Jed,Paul,Todd,Brandon,Hank,Jonathan,Peter,Wilbur,Amanda,Courtney,Heather,Melanie,Sara,Amber,Crystal,Katie,Meredith,Shannon,Betsy,Donna,Kristin,Nancy,Stephanie,Bobbie-Sue,Ellen,Lauren,Peggy,Sue-Ellen,Colleen,Emily,Megan,Rachel,Wendy".split(",")]

race_bias = ["black,blacks,Black,Blacks,African,african,Afro".split(","),
             "white,whites,White,Whites,Caucasian,caucasian,European,european,Anglo".split(",")]

religion_bias = ["baptism,messiah,catholicism,resurrection,christianity,salvation,protestant,gospel,trinity,jesus,christ,christian,cross,catholic,church".split(","),
                "allah,ramadan,turban,emir,salaam,sunni,koran,imam,sultan,prophet,veil,ayatollah,shiite,mosque,islam,sheik,muslim,muhammad".split(",")]
age_bias = ["Taylor,Jamie,Daniel,Aubrey,Alison,Miranda,Jacob,Arthur,Aaron,Ethan".split(","),
           "Ruth,William,Horace,Mary,Susie,Amy,John,Henry,Edward,Elizabeth".split(",")]

eco_bias = ["rich,richer,richest,affluence,advantaged,wealthy,costly,exorbitant,expensive,exquisite,extravagant,flush,invaluable,lavish,luxuriant,luxurious,luxury,moneyed,opulent,plush,precious,priceless,privileged,prosperous,classy".split(","),
           "poor,poorer,poorest,poverty,destitude,needy,impoverished,economical,inexpensive,ruined,cheap,penurious,underprivileged,penniless,valueless,penury,indigence,bankrupt,beggarly,moneyless,insolvent".split(",")]


bias_words = {"gender":gender_bias, "religion":religion_bias, "race":race_bias, "age":age_bias, "economic":eco_bias}

f = open("embedding4_Bias.json", "r")
biaswordEmbedding = json.loads(f.read())
f.close()

f = open("embedding4_Topic.json", "r")
topicwordEmbedding = json.loads(f.read())
f.close()

def groupBiasDirection(gp1, gp2): ### get the embedding for the bias words pair
    #print(gp1,gp2)
    dim = 786 ### BERT embedding is 786
    g1,g2 = np.zeros((dim,), dtype=float), np.zeros((dim,), dtype=float)
    cnt = 0
    for p in gp1: ### gp1 is a list, [black,blacks,Black,Blacks,African,african,Afro]
                  ### gp2 is a list, [white,whites,White,Whites,Caucasian,caucasian,European,european,Anglo]
        p = p.strip()
        if p not in biaswordEmbedding:
            continue
        p_vec = biaswordEmbedding[p]/norm(biaswordEmbedding[p])
        g1 = np.add(g1,p_vec)
        cnt += 1
    print("count:  ", cnt)

    cnt = 0
    for q in gp2:
        q = q.strip()
        if q not in biaswordEmbedding:
            continue
        q_vec = biaswordEmbedding[q]/norm(biaswordEmbedding[q])
        g2 = np.add(g2,q_vec) 
        cnt += 1
    print("count 2:  ", cnt)
    g1, g2 = g1/norm(g1), g2/norm(g2)
    return (g1,g2)


df = pd.DataFrame({"word":all_words})
for bias_type in bias_words:
    bias_w = bias_words[bias_type]
    df[bias_type] = None
    g1, g2 = groupBiasDirection(bias_w[0], bias_w[1])
    print("g1 is", g1)
    for index, row in df.iterrows():
        w = row["word"]
        print("w is", w)
        # assuming group bias "Quantification algo"
        df.at[index, bias_type] = round(cosine(g1,topicwordEmbedding[w])-cosine(g2,topicwordEmbedding[w]),4)
        break


gen_max, gen_min = df["gender"].max(), df["gender"].min()
#sen_max, sen_min = df["sentiment"].max(), df["sentiment"].min()
race_max, race_min = df["race"].max(), df["race"].min()
relg_max, relg_min = df["religion"].max(), df["religion"].min()
age_max, age_min = df["age"].max(), df["age"].min()
eco_max, eco_min = df["economic"].max(), df["economic"].min()

print("Gender: ",gen_min,gen_max)
#print("Sentiment: ",sen_min, sen_max)
print("Race: ",race_min, race_max)
print("Religion: ",relg_min, relg_max)
print("Age: ",age_min, age_max)
print("Economic: ",eco_min, eco_max)






def percentile_rank(values, col, negative=False):
    N = len(values)
    last_ind = -1
    for i,items in enumerate(values.iteritems()): 
        index, val = items[0], items[1]
        if last_ind!=-1 and val==df.at[last_ind, col]: 
            df.at[index, col] = df.at[last_ind, col] 
            #percentile.append(percentile[i-1])
        else:
            p = (N-i)/N
            #print(i,p)
            df.at[index, col] = p 
            #percentile.append(p)
        if negative:
            df.at[index, col] = df.at[index, col]*-1
        last_ind = index

for col in df.columns:
    if col=="word":
        continue
    values = df.loc[df[col]>0][col].sort_values(ascending=False, inplace=False)
    percentile_rank(values, col)
    
    values = df.loc[df[col]<0][col].sort_values(ascending=True, inplace=False)
    percentile_rank(values, col, negative=True)



gen_max, gen_min = df["gender"].max(), df["gender"].min()
#sen_max, sen_min = df["sentiment"].max(), df["sentiment"].min()
race_max, race_min = df["race"].max(), df["race"].min()
relg_max, relg_min = df["religion"].max(), df["religion"].min()
age_max, age_min = df["age"].max(), df["age"].min()
eco_max, eco_min = df["economic"].max(), df["economic"].min()

print("Gender: ",gen_min,gen_max)
#print("Sentiment: ",sen_min, sen_max)
print("Race: ",race_min, race_max)
print("Religion: ",relg_min, relg_max)
print("Age: ",age_min, age_max)
print("Economic: ",eco_min, eco_max)



# normalization of bias scores
for index, row in df.iterrows():    
    if row["gender"]>0:
        df.at[index, "gender"] = row["gender"]/gen_max
    else:
        df.at[index, "gender"] = -1*row["gender"]/gen_min
        
    if row["race"]>0:
        df.at[index, "race"] = row["race"]/race_max
    else:
        df.at[index, "race"] = -1*row["race"]/race_min
    
    #if row["sentiment"]>0:
    #    df.at[index, "sentiment"] = row["sentiment"]/sen_max
    #else:
    #    df.at[index, "sentiment"] = -1*row["sentiment"]/sen_min
        
    if row["religion"]>0:
        df.at[index, "religion"] = row["religion"]/relg_max
    else:
        df.at[index, "religion"] = -1*row["religion"]/relg_min
    
    if row["age"]>0:
        df.at[index, "age"] = row["age"]/age_max
    else:
        df.at[index, "age"] = -1*row["age"]/age_min  
    
    if row["economic"]>0:
        df.at[index, "economic"] = row["economic"]/eco_max
    else:
        df.at[index, "economic"] = -1*row["economic"]/eco_min  



gen_max, gen_min = df["gender"].max(), df["gender"].min()
#sen_max, sen_min = df["sentiment"].max(), df["sentiment"].min()
race_max, race_min = df["race"].max(), df["race"].min()
relg_max, relg_min = df["religion"].max(), df["religion"].min()
age_max, age_min = df["age"].max(), df["age"].min()
eco_max, eco_min = df["economic"].max(), df["economic"].min()

print("Gender: ",gen_min,gen_max)
#print("Sentiment: ",sen_min, sen_max)
print("Race: ",race_min, race_max)
print("Religion: ",relg_min, relg_max)
print("Age: ",age_min, age_max)
print("Economic: ",eco_min, eco_max)



df.to_csv("data/BERT_percentile.csv", encoding='utf-8', index=False)
