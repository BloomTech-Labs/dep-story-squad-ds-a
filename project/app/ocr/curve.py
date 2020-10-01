from text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length
#from google_handwriting_recognition.py import google_handwriting_recognizer_dir, google_handwriting_recognizer

string = "Great success. My name is Borat. I have come to America, to find Pamela Anderson, and \
        make her my wife. Very nice!"
string2 = "take in a database of URLs associated with particular usernames, store it in dictionary with scores,\
    append it to dict_list2, now should have list of dictionaries to scroll through"
string3 = " Once you have a list of dictionaries, you can scroll through each score related to each function, \
    one by one,  and get the data needed to start implementing the curve function, to then ultimately, \
        return star values for each player"
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

#print(store(string, "bill"))

# take in a database of URLs associated with particular usernames, store it in dictionary with scores,
#append it to dict_list2, now should have list of dictionaries to scroll through

'''
def insert(Database):
    
    In theory this takes a database, scrolls through each 
    URL in the database, uses google OCR to create text from the URL and receives corresponding Username,
    feeds the string and username into the store function, and appends it to a list of dictionaries, returns 
    the list
    
    dict_list = []
    for URL in Database:
        x = store(google_handwriting_recognizer(URL), URL:username)
        dict_list.append(x)
    return dict_list 
'''
# Once you have a list of dictionaries, you can scroll through each score related to each function, one by one,
# and get the data needed to start implementing the curve function, to then ultimately, return star values
# for each player

a = store(string, "bill" )
b = store(string2, "Kate")
c = store(string3, "Edward")
#print(a)
#print(b)
#print(c)

dictlist = []
dictlist.append(a)
dictlist.append(b)
dictlist.append(c)
#print(dictlist)

#for username in dictlist:
#    for name, scores in username.items():
#        for method, score in scores.items():
#            if method == "evaluate":
#                print(f"{name}, {method}:",score)
        
def compile(listofdicts, function)-> []: 
    '''
    takes in list of dictionaries, and function name, returns array of scores for that
    particular function
    '''
    scorelist = []
    for username in listofdicts:
        for name, scores in username.items():
            for method, score in scores.items():
                if method == function:
                    scorelist.append(score)
    return(scorelist)

print(compile(dictlist, "evaluate")) 
print("----------------")

def bigcompile(listofdicts):

    bigscorelist = []
    methodlist = set()
    #add different methods to methodlist
    for user in dictlist:
        for name, scores in user.items():
            #print(scores)
            for method, score in scores.items():
                methodlist.add(method)
    #for each method in the methodlist, compile, and append the lists to 
    #bigscorelist array
    for method in methodlist:
        x = compile(dictlist, method)
        bigscorelist.append(x)            
    #return a list of lists, each list representing a particular method                
    giantdictionary = dict(zip(methodlist, bigscorelist))
    
    return(giantdictionary)

print(bigcompile(dictlist))
#able to return a list of lists, based on dictionary lists    
