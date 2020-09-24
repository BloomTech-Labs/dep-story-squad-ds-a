from autocorrect import Speller
import re
import spacy
from spacy.tokenizer import Tokenizer
from nltk.stem import PorterStemmer

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
        elif part_of_speech == "VERB" or part_of_speech == "ADJ" or part_of_speech == "ADV" :
            count2 += 1

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
    by # of total words
    """
    original = len(tokenize(input_str))
    difference = original - spellchecked_words(input_str)

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
        x = len(arr2) / len(arr)

    return x


def avg_sentence_length(input_str: str) -> int:
    """
    finds average sentence length after tokenization
    by taking total tokens / tokens containing .
    """

    arr = []
    words = tokenize(input_str)
    count = 0
    for word in words:
        if '.' in word:
            count += 1

    for word in words:
        arr.append(word)
        x = (len(arr) / 10)

    return x / count


def avg_len_words(input_str: str) -> int:
    """
    finds the average length of words after tokenization in the text
    """
    arr = []
    words = tokenize(input_str)
    for word in words:
        x = len(word)
        arr.append(x)
        y = (sum(arr) / len(arr)) / 10

    return y


def evaluate(input_str: str) -> int:
    '''
    Evaluates text using unique words, avg len of words, avg sentence length, spelling efficiency,
    and descriptiveness to produce an overall score for the user
    '''
    score = (
            (.2 * unique_words(input_str)) +
            (.2 * avg_len_words(input_str)) +
            (.2 * avg_sentence_length(input_str)) +
            (.2 * efficiency(input_str)) +
            (.2 * descriptiveness(input_str))
        )

    return score


if __name__ == '__main__':
    # corrected = spellcheck(normal)
    # print("normal:", normal)
    # print()
    # print("corrected:", corrected)
    # x = google_pdf_handwriting_recognizer(local_path="./test_pdfs/test_pdf_1.pdf")
    # x = " ".join(x)
    string = "After a long toalk. ith the was Summer seperated Then side April was over. Suddenly before them. He mad at April that they diffeent sidles. from the on. Summer came running strong muscular mon stood a genie. I three wishes. was. onto completely a huge fla sh a Said. am here to grant you am made 2 w "
    x = (string)
    print(tokenize(x))
    print(avg_sentence_length(x))
    print(spellchecked_words(x))
    print(efficiency(x))
    print(unique_words(x))
    print(avg_len_words(x))
    print(evaluate(x))
    print(descriptiveness(x))
