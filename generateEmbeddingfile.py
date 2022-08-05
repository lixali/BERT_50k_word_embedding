import torch
from transformers import BertTokenizer, BertModel

# OPTIONAL: if you want to have more information on what's happening, activate the logger as follows
import logging
#logging.basicConfig(level=logging.INFO)

import matplotlib.pyplot as plt
#get_ipython().run_line_magic('matplotlib', 'inline')
import json
from collections import defaultdict
# Load pre-trained model tokenizer (vocabulary)
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')


# In[6]:


text = "Here is the sentence I want embedding for."
marked_text = "[CLS] " + text + " [SEP]"

# Tokenize our sentence with the BERT tokenizer.
tokenized_text = tokenizer.tokenize(marked_text)

# Print out the tokens.
print (tokenized_text)


# In[7]:


list(tokenizer.vocab.keys())[5000:5020]


# In[8]:


# Define a new example sentence with multiple meanings of the word "bank"
#text = "After stealing money from the bank vault, the bank robber was seen " \
       #"fishing on the Mississippi river bank."
#foundarticleshash

## data model inside "sentencesFiltered" {"nurse" : ["sentece1", "sentence2", "sentence3" ....]; "black": ["sentence1", "sentence2", "sentence3" ... ]}
## data model inside "tokenized_text" {"nurse": [["CLS", "fathers", "and", "mother", "refused", "to" ...], ["CLS", "made", "up", ....]]; "black": [] }
##                                                    ** sentence1**                                         ** sentence2

## data model inside "indexed_tokens" {"nurse": [[101,11397,1998,10756, .....], [101,11234,12342,16856, .....]]; "black": [[101,1137,12438,1142, .....], [101,1234,12342398,12346, .....]]}
##                                                    ** sentence1**                 ** sentence2

f = open ('sentenceFile_1.json', "r")
sentencesFiltered = json.loads(f.read())
f.close()

tokenized_text = defaultdict(list)
indexed_tokens = defaultdict(list)

def tokenizeSentence(sentencesFiltered):
    for word in sentencesFiltered:  ### word means topic/bias word here; not every single word in a sentence
        for idx in range(len(sentencesFiltered[word])):
            text = sentencesFiltered[word][idx] ### text is the sentence,

            # Add the special tokens.
            marked_text = "[CLS] " + text + " [SEP]"

            # Split the sentence into tokens.
            tokenizedText = tokenizer.tokenize(marked_text)
            if len(tokenizedText) > 512: 
                print("length of tokenizedText is ", len(tokenizedText))
                print(tokenizedText)
                #print(word, top50Articles[word])
                continue
            tokenized_text[word].append(tokenizedText) ### changed by lxiang

            # Map the token strings to their vocabulary indeces.
            indexed_tokens[word].append(tokenizer.convert_tokens_to_ids(tokenizedText)) ### changed by lixiang

            #if word == 'he' and len(tokenized_text[word][idx]) == 714:
            #    print(tokenized_text[word][idx])
            #print(tokenized_text[word][idx])
            # Display the words with their indeces.
            #for tup in zip(tokenized_text[word], indexed_tokens[word]):
            #    print('{:<12} {:>6,}'.format(tup[0], tup[1]))

    return [tokenized_text, indexed_tokens]
            
tokenizeSentence(sentencesFiltered)
print(tokenized_text)
#quit()

# In[9]:


### data model for "segments_ids" {"nurse": [[1, 1, 1, 1, ...], [1, 1, 1, 1, ...]]; "black": [[1, 1, 1, 1, ...], [1, 1, 1, 1, ...]] }
###                                                    ** sentence1**                                         ** sentence2

segments_ids = defaultdict(list)

def createSegmentsIds(tokenized_text):
    for word in tokenized_text:
        for idx in range(len(tokenized_text[word])):
            segments_ids[word].append([1] * len(tokenized_text[word][idx])) ### changed by lixiang ; tokenized_text[word][idx] is a sentece represented by a list of words

            print (segments_ids[word][idx])
            print(len(segments_ids[word][idx]))
        
createSegmentsIds(tokenized_text)


# In[10]:


# Convert inputs to PyTorch tensors

### data model for tokens_tensor is {"nurse": [tensor([[  101,  1000, 20934, ...]]), tensor([[  101,  7055,  1010 ... ]])]; "black": [tensor(), tensor()]}
###                                                    ** sentence1**                             ** sentence2


### data model for segments_tensors is {"nurse": [tensor([[1, 1, 1, 1, ...]]), tensor([[1, 1, 1, 1, ...]]), tensor(). ...]; "black": []};
###                                                    ** sentence1**                  ** sentence2

tokens_tensor = defaultdict(list)
segments_tensors = defaultdict(list)

def createTensor(indexed_tokens, segments_ids):
    for word in indexed_tokens:
        for idx in range(len(indexed_tokens[word])):
            #print(idx, indexed_tokens[word][idx])
            tokens_tensor[word].append(torch.tensor([indexed_tokens[word][idx]]))
            #print(idx, tokens_tensor[word][idx])
            #print(idx, len(segments_ids[word]))
            segments_tensors[word].append(torch.tensor([segments_ids[word][idx]]))
        print(len(tokens_tensor[word]), tokens_tensor[word])
        #print(len(segments_tensors[word]), segments_tensors[word])
        
     
createTensor(indexed_tokens, segments_ids)

'''
### debug one of the sentence in indexed_tokens['he'] is 714 problem
for i in range(len(indexed_tokens['he'])):
    print("length of the he sentence tokens is", len(indexed_tokens['he'][i]))

quit()
'''
# In[11]:


# Load pre-trained model (weights)
model = BertModel.from_pretrained('bert-base-uncased',
                                  output_hidden_states = True, # Whether the model returns all hidden-states.
                                  )

# Put the model in "evaluation" mode, meaning feed-forward operation.
model.eval()


# In[12]:


# Run the text through BERT, and collect all of the hidden states produced
# from all 12 layers. 

### data model for "hidden_states" is {"nurse": [(tensor([],[],...), tensor(), tensor() ... tensor()), (tensor(), tensor(), tensor() ... tensor())]
###                                     **sentence1** there are 13 tensors (as a tuple) in sentence1    ** sentence2 there are 13 tensors in sentence1


hidden_states = defaultdict(list)
hiddenStateFile = "./hiddenState.json"
hiddenstatef = open(hiddenStateFile,"a",encoding='utf-8')
def getHiddenState(tokens_tensor, segments_tensors):
    
    for word in tokens_tensor:
        for idx in range(min(len(tokens_tensor[word]),50)):
            with torch.no_grad():
                #print(word, tokens_tensor[word][idx].size(), segments_tensors[word][idx].size(), word)
                outputs = model(tokens_tensor[word][idx], segments_tensors[word][idx])

                # Evaluating the model will return a different number of objects based on 
                # how it's  configured in the `from_pretrained` call earlier. In this case, 
                # becase we set `output_hidden_states = True`, the third item will be the 
                # hidden states from all layers. See the documentation for more details:
                # https://huggingface.co/transformers/model_doc/bert.html#bertmodel
                hidden_states[word].append(outputs[2])
        #json_hiddenState_object = json.dumps({word: [t.cpu().detach().numpy().tolist() for t in hidden_states[word]]}, indent=4)
        #hiddenstatef.write(json_hiddenState_object)

    print(len(hidden_states["crime"]), hidden_states["crime"])
        
            
getHiddenState(tokens_tensor, segments_tensors)

hiddenstatef.close()

# In[13]:



def printHiddenState(hidden_states):
    for word in hidden_states:
        #print ("Number of layers:", len(hidden_states[word]), "  (initial embeddings + 12 BERT layers)")
        layer_i = 0

        #print ("Number of batches:", len(hidden_states[word][layer_i]))
        batch_i = 0

        #print ("Number of tokens:", len(hidden_states[word][layer_i][batch_i]))
        token_i = 0

        #print ("Number of hidden units:", len(hidden_states[word][layer_i][batch_i][token_i]))
        
printHiddenState(hidden_states)


# In[ ]:


# For the 5th token in our sentence, select its feature values from layer 5.
### token_i = 5 ### commented by Lixiang
### layer_i = 5 ### commented by Lixiang
### vec = hidden_states[layer_i][batch_i][token_i] ### commented by Lixiang

# Plot the values as a histogram to show their distribution.
#plt.figure(figsize=(10,10))
#plt.hist(vec, bins=200)
#plt.show()


# In[ ]:


# `hidden_states` is a Python list.
#print('      Type of hidden_states: ', type(hidden_states))

# Each layer in the list is a torch tensor.
#print('Tensor shape for each layer: ', hidden_states[0].size())


# In[ ]:


# Concatenate the tensors for all layers. We use `stack` here to
# create a new dimension in the tensor.

### data model for "token_embeddings" is {"nurse": [tensor([[1.6855e-01, -2.8577e-01, ...],[ 5.4667e-01, 3.3008e-01 ...], ... []), tensor() ]}
###                                                                ** sentence1****                                                 ** sentence2 


token_embeddings = defaultdict(list)
def createEmbedding(hidden_states):
    for word in hidden_states:
        for idx in range(len(hidden_states[word])):
            currentStack = torch.stack(hidden_states[word][idx], dim=0)
            token_embeddings[word].append(currentStack)

            currentStack.size()
    #print(len(token_embeddings["nurse"]), token_embeddings["nurse"])
    #print(len(token_embeddings["crime"]), token_embeddings["crime"])
        
createEmbedding(hidden_states)


# In[ ]:


torch.Size([13, 1, 22, 768])


# In[ ]:


# Remove dimension 1, the "batches".

def squeezeEmbedding(token_embeddings):
    for word in token_embeddings:
        for idx in range(len(token_embeddings[word])):
            token_embeddings[word][idx] = torch.squeeze(token_embeddings[word][idx], dim=1)

            token_embeddings[word][idx].size()
        
squeezeEmbedding(token_embeddings)


# In[ ]:


torch.Size([13, 22, 768])


# In[ ]:


# Swap dimensions 0 and 1.
def swapDimention(token_embeddings):
    for word in token_embeddings:
        for idx in range(len(token_embeddings[word])):
            token_embeddings[word][idx] = token_embeddings[word][idx].permute(1,0,2)

            token_embeddings[word][idx].size()
    
    #print(len(token_embeddings["nurse"]), token_embeddings["nurse"])
    #print(len(token_embeddings["crime"]), token_embeddings["crime"])
    
swapDimention(token_embeddings)


# In[ ]:


torch.Size([22, 13, 768])


# In[ ]:


# Stores the token vectors, with shape [22 x 3,072]
#token_vecs_cat = []
token_vecs_cat = defaultdict(list)

# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
def storeTokensVec(token_embeddings):
    for word in token_embeddings:
        for idx in range (len(token_embeddings[word])):
            token_vecs_cat[word].append([])
            for token in token_embeddings[word][idx]:

            # `token` is a [12 x 768] tensor
                #print("token length is" , len(token))
            # Concatenate the vectors (that is, append them together) from the last 
            # four layers.
            # Each layer vector is 768 values, so `cat_vec` is length 3,072.
                cat_vec = torch.cat((token[-1], token[-2], token[-3], token[-4]), dim=0)
                #print("cat_vec length is" , len(cat_vec))
                # Use `cat_vec` to represent `token`.
                token_vecs_cat[word][idx].append(cat_vec)

        print ('Shape is: %d x %d' % (len(token_vecs_cat[word][0]), len(token_vecs_cat[word][0][0])))
            
storeTokensVec(token_embeddings)


# In[ ]:


# Stores the token vectors, with shape [22 x 768]
#token_vecs_sum = []
token_vecs_sum = defaultdict(list)
# `token_embeddings` is a [22 x 12 x 768] tensor.

# For each token in the sentence...
def tokenVecSum(token_embeddings):
    for word in token_embeddings:
        for idx in range (len(token_embeddings[word])):
            token_vecs_sum[word].append([])
            for token in token_embeddings[word][idx]:

                # `token` is a [12 x 768] tensor

                # Sum the vectors from the last four layers.
                sum_vec = torch.sum(token[-4:], dim=0)

                # Use `sum_vec` to represent `token`.
                token_vecs_sum[word][idx].append(sum_vec)

        print ('Shape is: %d x %d' % (len(token_vecs_sum[word][0]), len(token_vecs_sum[word][0][0]))) ### token_vecs_sum[topic word][sentences][individual word]
        
tokenVecSum(token_embeddings)


# In[ ]:


# `hidden_states` has shape [13 x 1 x 22 x 768]
token_vecs = defaultdict(list)
# `token_vecs` is a tensor with shape [22 x 768]
sentence_embedding = defaultdict(list)

def sentenceEmbedding(hidden_states):
    for word in hidden_states:
        for idx in range(len(hidden_states[word])):
            token_vecs[word].append([])
            sentence_embedding[word].append([])
            token_vecs[word][idx] = hidden_states[word][idx][-2][0]

            # Calculate the average of all 22 token vectors.
            sentence_embedding[word][idx] = torch.mean(token_vecs[word][idx], dim=0)
        
sentenceEmbedding(hidden_states)


# In[ ]:


#printCount = 0
def printEmbeddingShape(sentence_embedding):
    for word in sentence_embedding:
        for idx in range(len(sentence_embedding[word])):
            print ("Our final sentence embedding vector of shape:", sentence_embedding[word][idx].size())
            #pass
            #printCount += 1
            #if printCount == 3: break

printEmbeddingShape(sentence_embedding)


# In[ ]:



def printTokenStr(tokenized_text):
    for word in tokenized_text:
        for idx, sentence in enumerate(tokenized_text[word]):
            for i, token_str in enumerate(sentence):
                if word == "nurse":
                    print (i, token_str)
                    #pass
        
printTokenStr(tokenized_text)
#print(tokenized_text)


# In[ ]:


import json

#print('')
#print("month  ", str(token_vecs_sum[6][:5]))
#print("in  ", str(token_vecs_sum[10][:5]))
#print("comes  ", str(token_vecs_sum[19][:5]))
file = "./embedding4_1.json"
notfoundEmbedding = open ('notfoundEmbedding.json', "w")


total = None
finalDict = {}
with open(file,"w",encoding='utf-8') as currfile:
    for word in token_vecs_sum:
        #if word == "janitor": print("current word and token_vecs_sum[word] is", word, token_vecs_sum[word])
        wordcount = 0
        total = None
        for idx, sentence in enumerate(token_vecs_sum[word]):
            for i, indiv_word_vec in enumerate(sentence):
                #if tokenized_text[word][idx][i] == "man":
                #    print("man is", tokenized_text[word][idx])
                #if tokenized_text[word][idx][i] == "janitor":
                #    print("janitor is", tokenized_text[word][idx])
                #if tokenized_text[word][idx][i] == word:
                if (i == len(tokenized_text[word][idx])-1 and tokenized_text[word][idx][i] == word.lower()) or (i+1 < len(tokenized_text[word][idx]) and tokenized_text[word][idx][i] == word.lower() and "#" not in tokenized_text[word][idx][i+1]):
                    wordcount += 1
                    if total == None: total = indiv_word_vec
                    else: total = torch.add(total, indiv_word_vec)
                elif (i < len(tokenized_text[word][idx]) and "#" in tokenized_text[word][idx][i]):
                    currstring = tokenized_text[word][idx][i-1]
                    curr_word_vec = sentence[i-1]
                    ydx = i
                    while ydx < len(tokenized_text[word][idx]) and "#" in tokenized_text[word][idx][ydx]:
                        currstring = currstring + tokenized_text[word][idx][ydx].replace("#","")
                        curr_word_vec += sentence[ydx]
                        ydx += 1

                    if currstring == word.lower():
                        wordcount += 1
                        if total == None: total = curr_word_vec
                        else: total = torch.add(total, curr_word_vec)
                        
                        
        if total != None: 
            #print(wordcount)
            total = torch.div(total, wordcount)
            totalArray = total.cpu().detach().numpy().tolist()
            #print(len(totalArray),totalArray)
            finalDict[word] = totalArray
            #currfile.write("%s\n" % total)
        else:
            notfoundEmbedding.write(word)
            print(tokenized_text[word])
            
    
    json_object = json.dumps(finalDict, indent=4)
    currfile.write(json_object)

notfoundEmbedding.close()