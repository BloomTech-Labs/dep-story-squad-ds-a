from autocorrect import Speller
import re
import spacy
#from spacy.tokenizer import Tokenizer
from nltk.stem import PorterStemmer
import json
from wordcount import wordlist

# initializing object
nlp = spacy.load("en_core_web_sm")
spell = Speller(lang='en')


def spellcheck(input_str: str) -> str:
    """
    Will scroll through string, correct spelling error words,
    and return the entire string
    """
    textcorrected = spell(input_str)

    return textcorrected


def tokenize(input_str: str) -> str:
    """
    Will return all individual words in an array, ignores NLP stop words
    """
    tokens = re.sub('[^a-zA-Z 0-9 \.]', '',  input_str)
    tokens = tokens.lower().split()
    STOP_WORDS = nlp.Defaults.stop_words
    arr = []
    for token in tokens:
        if token not in STOP_WORDS:
            arr.append(token)

    return arr


def descriptiveness(input_str: str) -> str:
    '''
    Spellchecks and tokenizes an input string in order to find part of speech of each word,
    compares verbs, adj, adv ratio to proper noun and noun ratio to describe how descriptive 
    the text is
    '''
    
    input_str2 = spellcheck(input_str)
    doc = nlp(input_str2)
    
    x = [token.pos_ for token in doc]
    count = 0
    count2 = 0 
    
    for part_of_speech in x:
        if part_of_speech == "PROPN" or part_of_speech == "NOUN" :
            count += 1

        elif part_of_speech == "VERB" or part_of_speech == "ADJ" :
            count2 += 1

    if count == 0:
        return 0
    elif count2 / count > 1:
        return 1

    else:
        return count2 / count


def spellchecked_words(input_str: str) -> int:
    '''
    Takes a string, runs spellcheck on string, compares
    different words after spellcheck to before,
    returns number of words spellchecked
    '''
    arr = []
    words1 = tokenize(input_str)
    words2 = tokenize(spellcheck(input_str))

    for word in words1:
        if word not in words2:
            arr.append(word)

    return len(arr)


def efficiency(input_str: str) -> int:
    """
    finds length of original string after tokenization,
    divides # of non-spellchecked words
    by # of total words, returns value between 0 and 1
    """
    original = len(tokenize(input_str))
    difference = original - spellchecked_words(input_str)
    if original == 0:
        return 0 
    else:
        percentage = difference / original
    
    return percentage


def unique_words(input_str: str) -> int:
    """
    finds percentage of total words in tokenized string that are unique words
    """
    arr = []
    arr2 = set()
    words = tokenize(input_str)
    for word in words:
        arr.append(word)
        arr2.add(word)
        if len(arr) == 0:
            return 0
        else:
            x = len(arr2) / len(arr)

    return x


def avg_sentence_length(input_str: str) -> int:
    """
    finds average sentence length after tokenization
    by taking total tokens / tokens containing .
    returns value between 0 and 1
    """

    arr = []
    words = tokenize(input_str)
    count = 0
    for word in words:
        if '.' in word:
            count += 1

    for word in words:
        arr.append(word)
        x = len(arr) 
        y = (x / 10)
    if count == 0:
        return 0 
    elif y > 1:
        return 1    
    else:
        return y / count


def avg_len_words(input_str: str) -> int:
    """
    finds the average length of words after tokenization in the text
    returns value between 0 and 1
    """
    arr = []
    words = tokenize(input_str)
    for word in words:
        x = len(word)
        arr.append(x)
        x = sum(arr) / len(arr)
        y = (x / 10)

        if len(arr) == 0:
            return 0
        elif y > 1:
            return 1    
        else:
            return y    

    
def vocab_length(input_str: str) -> int:
    '''
    Returns average word size of tokenized and unique words
    returns value between 0 and 1
    '''
    arr = set()
    arr2 = []
    words = tokenize(input_str)
    for word in words:
        arr.add(word)
        for word in arr:
            x = len(word)
            arr2.append(x)
            y = (sum(arr2) / len(arr2)) / 10
            if y == 0:
                return 0
            else:
                return y     
  
def good_vocab(input_str: str) -> int:
    '''
   Scrolls through input and matches up words against word list of large words,
   and returns percentage of words in input string that are in the word list,
   returns value between 0 and 1 
   '''
    arr = []
    arr2 = []
    words = tokenize(input_str)
    for word in words:
        arr2.append(word)
        if word in wordlist:
            arr.append(word)
            good_vocab = len(arr) / len(arr2)
    return good_vocab                       

def evaluate(input_str: str) -> int:
    '''
    Evaluates text using vocab score, avg sentence length, spelling efficiency,
    and descriptiveness to produce an overall score for the user
    '''
    score = (
            (.1 * vocab_length(input_str)) +
            (.2 * good_vocab(input_str)) +
            
            (.1 * avg_sentence_length(input_str)) +
            (.1 * efficiency(input_str)) +
            (.1 * descriptiveness(input_str))
        )

    return score
def good_vocab_stars(input_str: str) -> int:
    '''
    returns between 0 and 5 stars, rounded to the nearest half star, based on usage of 
    good vocabulary
    '''
    x = good_vocab(input_str) / .12
    y = round(x*2)/2
    if y >= 5:
        return 5
    else: 
        return y
def efficiency_stars(input_str: str) -> int:
    '''
    returns between 0 and 5 stars, rounded to the nearest half star, based on usage of 
    spellcheck efficiency
    '''
    x = efficiency(input_str) / .15
    y = round(x*2) / 2
    if y >= 5:
        return 5
    else: 
        return y
def word_length_stars(input_str: str) -> int:
    '''
    returns between 0 and 5 stars, rounded to the nearest half star, based on usage of 
    average word length
    '''
    x = vocab_length(input_str) / .15 
    y = round(x*2) / 2
    if y>=5:
        return 5
    else:
        return y  
def sentence_length_stars(input_str: str) -> int:
    '''
    returns between 0 and 5 stars, rounded to the nearest half star, based on usage of 
    avg sentence length
    '''
    x = avg_sentence_length(input_str) / .12
    y = round(x*2) / 2
    if y >= 5:
        return 5
    else:
        return y  
def descriptiveness_stars(input_str: str) -> int:
    '''
    returns between 0 and 5 stars, rounded to the nearest half star, based on usage of 
    descriptiveness
    '''
    x = descriptiveness(input_str) / .15
    y = round(x*2) / 2
    if y >=5:
        return 5
    else:
        return y                                

def store(input_str: str) -> str:
    str1 = vocab_length(input_str)
    str2 = avg_sentence_length(input_str)
    str3 = efficiency(input_str)
    str4 = descriptiveness(input_str)
    str5 = good_vocab(input_str)
    str6 = evaluate(input_str)

    jsonStr = json.dumps(str1)
    jsonStr2 = json.dumps(str2)
    jsonStr3 = json.dumps(str3)
    jsonStr4 = json.dumps(str4)
    jsonStr5 = json.dumps(str5)
    jsonStr6 = json.dumps(str6)
    storage = [ f"vocab_length: {(jsonStr)} ",  f"avg_sentence_length score: {(jsonStr2)}",  \
        f"efficiency score: {(jsonStr3)}" , f"descriptiveness score: {(jsonStr)} ",\
            f"good_vocab: {(jsonStr5)}", f"evaluate: {(jsonStr6)}"]
    
    return storage

if __name__ == '__main__':
    # corrected = spellcheck(normal)
    # print("normal:", normal)
    # print()
    # print("corrected:", corrected)
    # x = google_pdf_handwriting_recognizer(local_path="./test_pdfs/test_pdf_1.pdf")
    # x = " ".join(x)
    string = "Great success. My name is Borat. I have come to America, to find Pamela Anderson, and \
        make her my wife. Very nice!"
    x = (string)
    print(tokenize(x))
    #print(spellchecked_words(x))
    #print(unique_words(x))
    print(vocab_length(x))
    print(avg_sentence_length(x))
    print(efficiency(x))
    print(descriptiveness(x))
    print(good_vocab(x))
    print(evaluate(x))
    print(store(x))
    #print(wordlist)
    print(good_vocab_stars(x))
    print(efficiency_stars(x))
    print(word_length_stars(x))
    print(sentence_length_stars(x))
    print(descriptiveness_stars(x))