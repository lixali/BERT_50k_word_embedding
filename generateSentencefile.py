import subprocess
import json
from collections import defaultdict
f = open ('containfile_2.json', "r")
top50Articles = json.loads(f.read())
f.close()

# Reading from file
sentences = defaultdict(list)
#sentenceList = 
full = False
def splitIntoSentence(frequency):
    
    for word in frequency:
        full = False
        currentArticlesLength = min(len(frequency[word]), 50)
        #print(len(frequency[word]), 50)
        for idx in range(currentArticlesLength): ### only pick 50 articles; change it to 50; be careful, it is 50 articles; not 50 sentences
            if full == True: break
            file = frequency[word][idx]
            fileContailWord = False
            #print(word, frequency[word][idx], file)
            with open(file,"r",encoding='utf-8') as currfile:
                for line in currfile.readlines(): 
                    if full == True: break                       
                    if '"text":' in line:
                        a, b = line.split(":", 1)
                        #print(b)
                        b_list = b.split(". ")
                        for sentence in b_list:
                            if full == True: break
                            if word in sentence and len(sentence) < 512:
                                sentences[word] = [sentence]  ### changed by lixiang; this is a list of sentences
                                fileContailWord = True
                                full = True
                                
                                break
                        if fileContailWord == True: break
                
splitIntoSentence(top50Articles)
#quit()

# In[5]:

filteredSentenceFile = "./sentenceFile_2.json"
def writeFilteredSentence(sentences):

    with open(filteredSentenceFile, "w", encoding='utf-8') as filteredSentence:
        sentenceFildered_Object = json.dumps(sentences, indent = 4)
        filteredSentence.write(sentenceFildered_Object)

writeFilteredSentence(sentences)


#quit()