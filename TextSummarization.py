"""
Created on Wed Feb 22 17:54:44 2017

@author: Aisha
"""
from collections import defaultdict
from nltk.corpus import stopwords
import nltk
import string
import math
import operator 
import pickle
import os.path
import random
import re
from collections import namedtuple
from nltk.corpus import wordnet as wn

def SaveObject(objectToSave, filename):
    """
    Using pickle, save given object type into a pickle file
    
    Parameters
    ----------
    objectToSave: can be any type
        The variable to be save into a file
    name: string
        The filename
    
    Return
    -------
    None
    """
    with open(filename + '.pickle', 'wb') as handle:
        pickle.dump(objectToSave, handle, protocol=pickle.HIGHEST_PROTOCOL)

def LoadObject(filename):
    """
    Using pickle, load the given filename and return it as a variable
    
    Parameters
    ----------
    name: string
        The filename to load
    
    Return
    -------
    filetype of the variable loaded
        Return the loaded filetype as a variable, otherwise will return None
    """
    if(os.path.exists(filename + '.pickle')):
        with open(filename + '.pickle', 'rb') as handle:
            return pickle.load(handle)
    else:
        print("File does not exist")

def CreateDictionaryMovieReview(filename, startNumberProduct, endNumberOfProduct):
    """
    Open the Database which is a textfile. Extract all the data needed in the database and
    return a dictionary which has the productID and reviews
    
    Parameters
    ----------
    filename: string
        The filename of the database
        
    startNumberProduct: int
        the starting number of what product to extract. 
        i.e. if you put 100, it will start the 100th product ID
    
    endNumberOfProduct: int
        The ending number of the products to extract.
        i.i if you put 150, the function will end after getting the 150th product
        
    Return
    -------
    defaultdict(str)
        returns a defaultdict where the keys are the productID and 
        the values are the reviews of that product
    """
    file = open(filename, 'r', encoding='latin-1') #Open the text database
    
    productID = ""
    currentProductNumber = 0 
    reviews = defaultdict(str)
    
    for x in file:
        if (x[:18] == "product/productId:"): #extract the product ID
            if(productID != x[19:-1]):
                currentProductNumber += 1
            productID = x[19:-1]
        if(currentProductNumber < startNumberProduct): #use to skip the preceding products before the starting point
            continue
        elif (x[:12] == "review/text:"): #extract the reviews of the product
            review = x[13:]
        elif (x == "\n"): #remove unnecessary artifacts and put the product in the dictionary
            review = re.sub('<[^>]+>', '', review)
            review = re.sub('&[^;]+;', '', review)
            review = review.replace('\\n', ' ' )
            review = review.replace('\\', '' )
            review = re.sub(r'\.([A-Z])', r'. \1', review)
            reviews[productID] += " " + review
        if currentProductNumber > endNumberOfProduct: #edd loop if ending point is reached
            break 

    file.close()
    return reviews

def ProcessDocumentToWordList(document):
    """
    Given a string document, remove all unnecessary characters 
    in order to seperate the words correctly into a word list.
    
    Parameters
    ----------
    document: string
        the document to be made into a word list
        
    Return
    -------
    list(str)
        returns a list of words
    """
    document = document.replace('[', ' ')
    document = document.replace('(', ' ')
    document = document.replace(')', ' ')
    document = document.replace(']', ' ')
    document = document.replace('-', ' ')
    document = document.replace('"', ' ')
    document = document.replace(':', ' ')
    document = document.replace('!', ' ')
    document = document.replace('?', ' ')
    document = document.replace('. ', ' ')
    document = document.replace('\\n', ' ' )
    document = document.replace('\\', '' )
    document = document.lower()
    document = ' '.join(document.split())
    
    return document.split()
    
def ProcessDocumentIntoTermDocumentFrequency(document, termDocumentFrequency, numberOfDocuments):
    """
    Given a document, process the document and update the terms value in the term document frequency dictionary
    
    Parameters
    ----------
    document: string
        the document to be process in the term document frequency dictionary
    
    termDocumentFrequency: dict(int)
        A dictionary with keys that consist of a word string and the values 
        as the number of documents that contains that key word string
        
    numberOfDocuments: int
        The number of numberOfDocuments in the term document frequency dictionary
        
    Return
    -------
    int
        returns the number of documents in the term document frequency dictionary
    """
    for word in set(ProcessDocumentToWordList(document)): #convert into a set to remove duplicate words
        if word in termDocumentFrequency:
            termDocumentFrequency[word] += 1
        else:
            termDocumentFrequency[word] = 1 #if the word is not in the dictionary, create it and add it
    numberOfDocuments += 1
    return numberOfDocuments


def UpdateCorpus(dictionaryMovieReview, corpus):
    """
    Given a database of documents and the corpus. Process the database and update the corpus
    
    Parameters
    ----------
    dictionaryMovieReview: dict(str)
        A dictionary with the key as the product ID and values as a collection of reviews of that product 
    
    corpus: namedtuple("Corpus", "termDocumentFrequency numberOfDocuments productIDList")
        A namedtuple that contains a dictionary where the key is a word and 
        value is the number of document with that word, the number of documents in the dictionary,
        and the list of productsID, each documents has a product ID and the list will help to see what products are in the corpus

    Return
    -------
    namedtuple("Corpus", "termDocumentFrequency numberOfDocuments productIDList")
        returns the updated corpus
    """
    for productID in dictionaryMovieReview:
        if(productID not in corpus.productIDList):
            corpus.productIDList.append(productID)            
            corpus = corpus._replace(numberOfDocuments = ProcessDocumentIntoTermDocumentFrequency(dictionaryMovieReview[productID], corpus.termDocumentFrequency, corpus.numberOfDocuments))            
    return corpus
    
def RemoveStopwords(document): 
    """
    Given a document, return a list of words with the stop word removed.
    
    Parameters
    ----------
    document: str
        The document to be process into a list of words with not stop word
    
    Return
    -------
    list(str)
        returns a list of words with no stop word 
    """
    document = ProcessDocumentToWordList(document)
    document = ' '.join(document)
    
    document = re.sub(r'[^\w]', ' ', document)
    word_list = [] 
    for lines in document.split():
        for words in lines.lower().split():
            if words not in stopwords.words('english'):
                word_list.append(words)
    for s in string.punctuation:
        for w in range(len(word_list)): 
            if s in word_list[w]: 
                word_list[w] = word_list[w].replace(s, "")
    
    for x in word_list:
        if x in stopwords.words('english'):
            word_list.remove(x)
    word_list = list(filter(None, word_list))
    
    return word_list

def GenerateWordFrequency(wordList): 
    """
    Given a list of words, return a sorted list tuple that counts each words
    
    Parameters
    ----------
    wordList: list(str)
        The list of words to sort and count
    
    Return
    -------
    list(tuple(str, int))
        returns a sorted list, sorted based on the highest number of words in the given word list
    """
    fdist = nltk.FreqDist(wordList).most_common() #Use freqdist to find how often the words occurred in the text
    freq = []
    for (x, y) in fdist: 
        if int(y) > 1:
            freq.append((x,y))

    return freq
    

def TokenizeSentences(document):
    """
    Given a document, seperate the document into a list of sentences and return that list
    
    Parameters
    ----------
    document: str
        The document that will be seperated into a list of sentences
    
    Return
    -------
    list(str)
        returns a list of sentences, processed from the document string
    """
    sentenceList = [] 
    
    sentences = nltk.sent_tokenize(document)
    for sentence in sentences: 
        #sentence = re.sub(r'[^\w]', ' ', sentence)
        sentenceList.append(sentence)
    return sentenceList            

def CalculateTfidf(wordFrequency, termDocumentFrequency, numberOfDocuments):
    """
    Calculate the tfidf of each words and return those words with the tfidf values calculated
    
    Parameters
    ----------
    wordFrequency: list(tuple(str, int))
        A list detailing the frequency of each word
        
    termDocumentFrequency: dict(value)
        A dictionary that store words and how many documents in the corpus that contains that word
        
    numberOfDocuments: int
        the number of documents in the corpus
    
    Return
    -------
    dict(float)
        returns a tfidf dictionary, that contains the word and it's tfidf value
    """
    tfidf = dict()
    for word, freq in wordFrequency:
        if word in termDocumentFrequency:      
            tfidf[word] = abs(freq * math.log(numberOfDocuments / (1 + termDocumentFrequency[word])))
        else:
            tfidf[word] = abs(freq * math.log(numberOfDocuments / 1))
    return tfidf

    
def TfidfScoreSentences(tfidf, sentenceList, useOnlyNouns, takeLengthIntoAccount):
    """
    Calculate the score of each sentence using the tfidf value of the words in that sentence
    
    Parameters
    ----------
    tfidf: dict(float)
        A dictionary containing words and it's tfidf values
        
    sentenceList: list(str)
        A list of senteces to be scored
        
    useOnlyNouns: bool
        if true will only calculate words that are considered as a noun
    
    Return
    -------
    dict(float)
        returns a dictionary of sentences with it's calculated tfidf based score
    """
    nouns = {x.name().split('.', 1)[0] for x in wn.all_synsets('n')}
    
    totalTfidfValue = sum(tfidf.values())

    sentenceScoreDictionary = {} 
    for sentence in sentenceList:
        calculate_score = 0
        for word in ProcessDocumentToWordList(sentence):
            if useOnlyNouns:
                if word in tfidf and word in nouns:
                    calculate_score += tfidf[word]
            else:
                if word in tfidf:
                    calculate_score += tfidf[word]
        if takeLengthIntoAccount:
            sentenceScoreDictionary[sentence] =  math.pow((calculate_score / totalTfidfValue),2) / len(sentence.split())
        else:
            sentenceScoreDictionary[sentence] =  calculate_score / totalTfidfValue
    return sentenceScoreDictionary

def LuhnScoreSentences(wordFrequency, sentenceList):
    """
    Calculate the score of each sentence using the Luhn algorithm
    
    Parameters
    ----------
    wordFrequency: list(tuple(str, int))
        A list detailing the frequency of each word
        
    sentenceList: list(str)
        A list of senteces to be scored
    
    Return
    -------
    dict(float)
        returns a dictionary of sentences with it's calculated score based on the Luhn algorithm
    """
    sentenceScoreDictionary = defaultdict(float)
    
    tenthPercentOfLengthOfFrenquency = 0.10 * len(wordFrequency)
    wordFrequency[:int(round(tenthPercentOfLengthOfFrenquency))]
    
    for sentence in sentenceList:
        wordCount = 0
        processSentence = ProcessDocumentToWordList(sentence)
        for word, frequency in wordFrequency: 
            if word in processSentence:
                wordCount += 1        
        sentenceScoreDictionary[sentence] = math.pow(wordCount,2) / len(sentence.split())    
    
    return sentenceScoreDictionary
    
def PrintSummary(sentenceScoreDictionary, numberOfSentence):
    """
    Given a dictionary of sentences with a calculated score. Print a summary
    
    Parameters
    ----------
    sentenceScoreDictionary: dict(float)
        A dictionary containing the sentences and its calculated score
        
    numberOfSentence: int
        The number of sentences in the generated summary
    
    Return
    -------
    None
    """
    summary = "" 
    sortedSentencesTuple = sorted(sentenceScoreDictionary.items(), key=operator.itemgetter(1), reverse=True) 
    sortedSentenceWithoutScore = [x for (x,y) in sortedSentencesTuple]

    for sentence in sortedSentenceWithoutScore[:numberOfSentence]: 
        sentence = ' '.join(sentence.split())
        summary += sentence.strip() + " " 
    print(summary)

def PrintRandomSummary(sentenceList, numberOfSentence):
    """
    Randomly pick sentences from a list and print a summary
    
    Parameters
    ----------
    sentenceList: list(str)
        A list of sentences
        
    numberOfSentence: int
        The number of sentences in the generated summary
    
    Return
    -------
    None
    """
    summary = "" 
    randomSentences = list()
    
    while(len(randomSentences) <= numberOfSentence):
        randomSentences.append(random.choice(sentenceList))
        
    for sentence in randomSentences:
        sentence = ' '.join(sentence.split())
        summary += sentence.strip() + " " 

    
    print(summary)

def GenerateTFIDF(documentToSummarize, corpus, numberOfSentenceInSummary, useOnlyNouns, takeLengthIntoAccount):
    """
    Given the neccesary parameters, generate a summary using the tfidf algorithm
    
    Parameters
    ----------
    documentToSummarize: str
        The document to summirize
        
    corpus: namedtuple("Corpus", "termDocumentFrequency numberOfDocuments productIDList")
        The corpus
        
    numberOfSentenceInSummary: int
        The number of sentence in the summary
        
    useOnlyNouns: bool
        Generate a summary using only the values of words that are noun
    
    takeLengthIntoAccount: bool
        Longer sentences will not have any advantage if this is set to true
    Return
    -------
    None
    """
    sentenceList = TokenizeSentences(documentToSummarize)   
    wordFrequency = GenerateWordFrequency(ProcessDocumentToWordList(documentToSummarize))
    tfidf = CalculateTfidf(wordFrequency, corpus.termDocumentFrequency, corpus.numberOfDocuments)
    PrintSummary(TfidfScoreSentences(tfidf, sentenceList, useOnlyNouns, takeLengthIntoAccount), numberOfSentenceInSummary)

def GenerateLuhn(documentToSummarize, numberOfSentenceInSummary):
    """
    Given the neccesary parameters, generate a summary using the Luhn algorithm
    
    Parameters
    ----------
    documentToSummarize: str
        The document to summirize
        
    numberOfSentenceInSummary: int
        The number of sentence in the summary
    
    Return
    -------
    None
    """
    sentenceList = TokenizeSentences(documentToSummarize)
    wordListWithStopWordRemoved = RemoveStopwords(documentToSummarize)
    wordFrequency = GenerateWordFrequency(wordListWithStopWordRemoved)
    PrintSummary(LuhnScoreSentences(wordFrequency, sentenceList), numberOfSentenceInSummary)
    
def GenerateRandomSummary(documentToSummarize, numberOfSentenceInSummary):
    """
    Generate a summary by randomaly picking sentences from the document
    
    Parameters
    ----------
    documentToSummarize: str
        The document to summirize
        
    numberOfSentenceInSummary: int
        The number of sentence in the summary
    
    Return
    -------
    None
    """
    sentenceList = TokenizeSentences(documentToSummarize)
    PrintRandomSummary(sentenceList, numberOfSentenceInSummary)

