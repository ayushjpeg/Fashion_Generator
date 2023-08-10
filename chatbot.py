from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

import sys
import keyboard
import json
import ast
import itertools
import numpy as np
from pandas import json_normalize
import pickle
import ipyplot


import nltk
import pickle
from transformers import pipeline
from nltk.stem import PorterStemmer
from simcse import SimCSE

# Load NLTK resources
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("averaged_perceptron_tagger")
nltk.download("wordnet")

# Initialize NLTK resources
ps = PorterStemmer()

# Load semantic classification model
model_semantick_id = "PriaPillai/distilbert-base-uncased-finetuned-query"
classifier_sem = pipeline("text-classification", model=model_semantick_id)

# Load SimCSE model
model_SIMCSE = SimCSE("princeton-nlp/sup-simcse-roberta-large")
with open('index.pkl', 'rb') as f:
    index = pickle.load(f)
model_SIMCSE.index = index
items = index['sentences']


model_id = "rasta/distilbert-base-uncased-finetuned-fashion"
classifier = pipeline("text-classification", model=model_id)

def classify(text):
    preds = classifier(text, top_k=None)
    if preds[0]['score']  <= preds[1]['score']:
        return "Not Fashion"
    else:
        return "Fashion"
    
def attribute_extraction(txt):
    tokenized = sent_tokenize(txt)

    attributes = []
    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)

    for i,w in enumerate(tagged) :
        if w[1] in ['NN','NNS','RB'] :
            ind =i 
            attr = w[0]
            while tagged[ind-1][1] in ['JJ','VBN','NN','RB','VBD','EX']:
                    attr = tagged[ind-1][0] + ' ' +  attr
                    ind = ind - 1
                    
            if len(attr.split())==1 and txt.split()[0].lower()=='will':
                attr = tagged[ind-1][0] + ' ' +  attr
                
            if classify(attr) == 'Fashion':
                attributes.append(attr)
            for a in attributes:
                for b in attributes:
                    if (a!=b) and (a in b):
                        attributes.remove(a)
                
            for a in attributes:
                if 'fit' in a :
                    attributes = list(map(lambda x: x.replace(a, a.replace(' fit','')), attributes))
                if 'match' in a :  
                    attributes = list(map(lambda x: x.replace(a, a.replace(' match','')), attributes))                                       
                
    return attributes        


posts = nltk.corpus.nps_chat.xml_posts()[:10000]

def dialogue_act_features(post):
    features = {}
    for word in nltk.word_tokenize(post):
        features['contains({})'.format(word.lower())] = True
    return features

featuresets = [(dialogue_act_features(post.text), post.get('class')) for post in posts]

# 10% of the total data
size = int(len(featuresets) * 0.1)

# first 10% for test_set to check the accuracy, and rest 90% after the first 10% for training
train_set, test_set = featuresets[size:], featuresets[:size]

# get the classifer from the training set
classifiers = nltk.NaiveBayesClassifier.train(train_set)
# to check the accuracy - 0.67
# print(nltk.classify.accuracy(classifier, test_set))

question_types = ["whQuestion","ynQuestion"]
def is_ques_using_nltk(ques):
    question_type = classifiers.classify(dialogue_act_features(ques)) 
    return question_type in question_types


question_pattern = ["do i", "do you", "what", "who", "is it", "why","would you", "how","is there",
                    "are there", "is it so", "is this true" ,"to know", "is that true", "are we", "am i", 
                   "question is", "tell me more", "can i", "can we", "tell me", "can you explain",
                   "question","answer", "questions", "answers", "ask"]

helping_verbs = ["is","am","can", "are", "do", "does"]
# check with custom pipeline if still this is a question mark it as a question

def is_question(question):
    question = question.lower().strip()
    if not is_ques_using_nltk(question):
        is_ques = False
        # check if any of pattern exist in sentence
        for pattern in question_pattern:
            is_ques  = pattern in question
            if is_ques:
                break

        # there could be multiple sentences so divide the sentence
        sentence_arr = question.split(".")
        for sentence in sentence_arr:
            if len(sentence.strip()):
                # if question ends with ? or start with any helping verb
                # word_tokenize will strip by default
                first_word = nltk.word_tokenize(sentence)[0]
                if sentence.endswith("?") or first_word in helping_verbs:
                    is_ques = True
                    break
        return is_ques    
    else:
        return True
    
from transformers import pipeline
import pandas as pd
import matplotlib.pyplot as plt
from nltk.stem import PorterStemmer


model_semantick_id = "PriaPillai/distilbert-base-uncased-finetuned-query"
classifier_sem = pipeline("text-classification", model=model_semantick_id)


ps = PorterStemmer()
verb_pattern = [ps.stem(i) for i in ['match', 'suit', 'fit', 'wear', 'pair']]
# 'be', 'go', 'are'

def semantic_check_hard_coded(txt):
    tokenized = sent_tokenize(txt)
    verbs = []
    
    for i in tokenized:
        wordsList = nltk.word_tokenize(i)
        tagged = nltk.pos_tag(wordsList)

    for i,w in enumerate(tagged) :
        if w[1] in ['VB','VBD','VBN','VBG','VBP','VBZ'] :
            verbs.append(ps.stem(w[0]))
    
    for v in verbs:
        if v in verb_pattern :
            return True
    return False

def semantic_check(text):
    if semantic_check_hard_coded(text):
        return True
    preds = classifier_sem(text, top_k=None)
    print(preds)
    if preds[0]['score']  <= preds[1]['score']:
        return True
    else:
        return False
    
def extraction_pipeline(query):
    if not is_question(query):
        message = "I am not understanding you, please enter a question that is related to fashion"
        return message, []
    elif not semantic_check(query) :
        message = "I am not sure to get your query can you please try again ?"
        return message, []
    else:
        return "Working ...",attribute_extraction(query)

def garment_matching(attr,k):           # Returns k best matches to the given attribute
    
    attr = " ".join([lemmatizer.lemmatize(i) for i in attr.split()])
    i= 0
    match = []

    if attr in items:
        if k == 5 :
            match,i = matrix_search_match(attr,k)
        if k == 10 :
            match,i = matrix_search_advice(attr,k)

    else :
        similar = similar_items(attr)
        stop = False
        ind = 0
        while (not stop) and (ind < len(similar)):
            print(len(similar))
            if similar[ind] in items:
                if k == 5:
                    match,i = matrix_search_match(similar[ind],k)
                if k == 10:
                    match,i = matrix_search_advice(similar[ind],k)
                if (i>0):
                    stop = True 
                    attr = similar[ind]
            ind = ind + 1

    if (i==0):
        message = 'This attribute was not found for the garment matching try another attribute!'
        return message,[]
        
    return attr,match

def garment_advice(attr1 , attr2, k=10):
    match = []
    
    i = 0
    attr1, match = garment_matching(attr1,k)
    
    #attr2 = " ".join([lemmatizer.lemmatize(i) for i in attr2.split()])
    
    if match is None :
        return attr1,None, False
    
    if attr2 in match:
        return attr1,attr2,True
    else:
        for el in match:
            if model_SIMCSE.similarity(el,attr2) > 0.9 :
                return attr1,el,True
    
    return None, None, False


user_input = input("Enter your fashion query: ").lower()

def main():
    user_input = input("Enter your fashion query: ").lower()

    if is_question(user_input):
        if semantic_check(user_input):
            message, attr = attribute_extraction(user_input)
            if not attr:
                print(message)
            else:
                print(message)
                print("Would you like garment matching or advice?")

        else:
            print("I'm not sure I understand your query. Can you please rephrase it?")

    else:
        print("I'm not sure what you're asking. Can you please rephrase your question or query?")

if __name__ == "__main__":
    main()