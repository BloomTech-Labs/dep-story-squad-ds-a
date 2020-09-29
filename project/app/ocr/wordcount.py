import nltk
#nltk.download()
from nltk.book import *
import spacy
import re
nlp = spacy.load("en_core_web_sm")


#print(text1.concordance("monstrous"))
print(len(text1))
print(len(text2))
print(len(set(text3)) / len(text3))

a = set(text1)
b = set(text2)
c = set(text3)
d = set(text4)
e = set(text5)
f = set(text6)
g = set(text7)
h = set(text8)
i = set(text9)

wordlist = []
j = a|b|c|d|e|f|g|h|i
for word in j :
    if len(word) >= 5 and word.islower() and word.isalpha():
        wordlist.append(word)

print(len(wordlist))  





