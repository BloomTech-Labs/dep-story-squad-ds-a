#import nltk
# nltk.download()
#from nltk.book import *
import spacy
import re


nlp = spacy.load("en_core_web_sm")

#fdist1 = FreqDist(text1)
#fdist2 = FreqDist(text2)
#fdist3 = FreqDist(text3)
#fdist4 = FreqDist(text4)
#fdist5 = FreqDist(text5)
#fdist6 = FreqDist(text6)
#fdist7 = FreqDist(text7)
#fdist8 = FreqDist(text8)
#fdist9 = FreqDist(text9)



#print(text1.concordance("monstrous"))
#print(len(text1))
#print(len(text2))
#print(len(set(text3)) / len(text3))

#a = set(text1)
#b = set(text2)
#c = set(text3)
#d = set(text4)
#e = set(text5)
#f = set(text6)
#g = set(text7)
#h = set(text8)
#i = set(text9)
#a1 = text1
#a2 = text2
#a3 = text3
#a4 = text4
#a5 = text5
#a6 = text6
#a7 = text7
#a8 = text8
#a9 = text9


#wordlist = []
#j = a|b|c|d|e|f|g|h|i

########
#jesse_words = j

# print("starting to read hadi's file")

with open("app/ocr/words.txt") as file_obj:

    words = file_obj.readlines()

wordlist = []
for x in words :
    if (len(x) >= 5 and x.strip().isalpha()):
        wordlist.append(x.strip().lower())

# print("ending hadi's file reading")

#for word in j :
#    if len(word) > 5 and word.islower() and word.isalpha():

#        wordlist.append(word)

#print(len(wordlist))  

#def avg_size(arr=[]):
#    size = []
#    for word in arr:
#        size.append(len(word))
#        count = 0
#        for x in size:
#            count += x
#            return(count / len(size))

# print(len(wordlist))       
        

    
    

#x = [word for word in j if FreqDist(word) < 50]
#print(x)


#print(len(b2))



