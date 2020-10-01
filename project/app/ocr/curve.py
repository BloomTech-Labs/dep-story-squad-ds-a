from text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length
from google_handwriting_recognition.py import google_handwriting_recognizer_dir, google_handwriting_recognizer

string = "Great success. My name is Borat. I have come to America, to find Pamela Anderson, and \
        make her my wife. Very nice!"


def store(input_str: str,  username: str) -> int:
    d = {
        username: {
            "evaluate": evaluate(input_str),
            "good_vocab_stars": good_vocab(input_str),
            "efficiency_stars": efficiency(input_str),
            "decriptiveness_stars": descriptiveness(input_str),
            "sentence_length_stars": avg_sentence_length(input_str),
            "word_length_stars": vocab_length(input_str)
            }
        }           
    return d    

print(store(string, "bill"))

# take in a database of URLs associated with particular usernames, store it in dictionary with scores,
#append it to dict_list2, now should have list of dictionaries to scroll through


def insert(Database):
    '''
    In theory this takes a database, scrolls through each 
    URL in the database, uses google OCR to create text from the URL and receives corresponding Username,
    feeds the string and username into the store function, and appends it to a list of dictionaries, returns 
    the list
    '''
    dict_list = []
    for URL in Database:
        x = store(google_handwriting_recognizer(URL), URL:username)
        dict_list.append(x)
    return dict_list 

# Once you have a list of dictionaries, you can scroll through each score related to each function, one by one,
# and get the data needed to start implementing the curve function, to then ultimately, return star values
# for each player



