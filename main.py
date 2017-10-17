# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 20:44:38 2017

@author: Aisha
"""

"""
How to use:
    First set save and resetVariable to true. This will make the neccesary files to do the summarization.
    Both variables can then be set to false for faster execution.    
    Set viewProductID to true to see available product IDs.
    Put desired product to summarize in the productIDtoGenerate variable as a string.
"""


from TextSummarization import *
#===========Main=============#
Corpus = namedtuple("Corpus", "termDocumentFrequency numberOfDocuments productIDList")




#starting number and ending number are created in order to partially save documents in the corpus
#i.e. you start doing the first ten thousand first, set save to true in order to save the variables 
#and then do startingNumber = 10000, endingNumber = 20000, save the variables in order to do the next ten thousand
startingNumber = 0
endingNumber = 10000
productIDtoGenerate = "B009NQKPUW"
numberOfSentenceInSummary = 5

#Set to true if the variables are not to be loaded and be reset
resetVariable = False

#Set to true if the variables are to be saved. Needed to be true in beginning when there are no variables to be loaded
save = False

#Set to true in order to see available product IDs
viewProductID = True
    
if(os.path.exists("dictionaryMovieReview" + '.pickle')):
    dictionaryMovieReview = LoadObject("dictionaryMovieReview")
else:
    dictionaryMovieReview = defaultdict(str)
if(os.path.exists("corpus" + '.pickle')):
    corpus = LoadObject("corpus")
else:
    corpus = Corpus(dict(), 0, list())

if resetVariable:
    dictionaryMovieReview = defaultdict(str)
    corpus = Corpus(dict(), 0, list())
    
if save:
    dictionaryMovieReview.update(CreateDictionaryMovieReview("movies.txt", startingNumber, endingNumber))
    corpus = UpdateCorpus(dictionaryMovieReview, corpus)
    SaveObject(dictionaryMovieReview, "dictionaryMovieReview")    
    SaveObject(corpus, "corpus")

productIDLength = []
if viewProductID:
    for productID in dictionaryMovieReview:
        productIDLength.append((productID, len(dictionaryMovieReview[productID])))
    print(sorted(productIDLength, key=lambda tup: tup[1]))
    
documentToSummarize = dictionaryMovieReview[productIDtoGenerate]

#print("======TFIDF======")
#GenerateTFIDF(documentToSummarize, corpus, numberOfSentenceInSummary, False, False)
#print()
#
#print("======TFIDF using only nouns======")
#GenerateTFIDF(documentToSummarize, corpus, numberOfSentenceInSummary, True, False)
#print()

print("======TFIDF with length taken into account======")
GenerateTFIDF(documentToSummarize, corpus, numberOfSentenceInSummary, False, True)
print()

print("======TFIDF using only nouns and length taken into account======")
GenerateTFIDF(documentToSummarize, corpus, numberOfSentenceInSummary, True, True)
print()


print("======Luhn======")
GenerateLuhn(documentToSummarize, numberOfSentenceInSummary)
print()

print("======Random Sentences======")
GenerateRandomSummary(documentToSummarize, numberOfSentenceInSummary)