from text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length
import numpy as np         
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
            "good_vocab": good_vocab(input_str),
            "efficiency": efficiency(input_str),
            "decriptiveness": descriptiveness(input_str),
            "sentence_length": avg_sentence_length(input_str),
            "word_length": vocab_length(input_str)
            }
        }           
    return d    

#print(store(string, "bill"))

# take in a database of URLs associated with particular usernames, store it in dictionary with scores,
#append it to dict_list2, now should have list of dictionaries to scroll through

'''
def create_dictlist(Database):
    
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
        
def compiler(listofdicts, function)-> []: 
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
    #for given function name, scrolls through list of nested dictionaries, returns all values to an array
    #returns the array of scores
    return(scorelist)

print(compiler(dictlist, "evaluate")) 
print("----------------")

def bigcompile(listofdicts):

    bigscorelist = []
    methodlist = []
    #add different methods to methodlist
    for user in dictlist:
        for name, scores in user.items():
            for method, score in scores.items():
                if method not in methodlist:
                    methodlist.append(method)
    #for each method in the methodlist, compile, and append the lists to 
    #bigscorelist array
    for method in methodlist:
        x = compiler(dictlist, method)
        bigscorelist.append(x)            
    #return a dictionary object with all methods and their corresponding arrays               
    giantdictionary = dict(zip(methodlist, bigscorelist))
    
    return(giantdictionary)
    
print(dictlist)
print("------------------------------")
x = bigcompile(dictlist)
print(x)
print("---------------------------")
#able to return a list of lists, based on dictionary lists   
# 
# Now we can start doing math on the individual functions and their lists, within the big dictionary
# 

#This simply requires you to scroll through each array, find the max, return the max as an adjuster
def maxscorelist(dictlist):
    #arrange dictionary into methods, and arrays of corresponding scores
    x = bigcompile(dictlist)
    maxscorelist = []
    for method, scores in x.items():
        score = np.max(scores)
        maxscorelist.append(score)
    #append high score from each corresponding array to maxscore array, return array
        
    return(maxscorelist)

print(maxscorelist(dictlist)) 
print("-----------------------------") 


def finalscore(dictlist, userid):
    #calculates adjusted curved scored for particular user and particular dictionary list
    #gets maximum score array for entire dictionary list
    y = maxscorelist(dictlist)
    
    individ_scores = []
    
    for entry in dictlist:
        for user, scores in entry.items():
            if user == userid:
                for method, score in scores.items():
                    individ_scores.append(score)
    #take individual user scores and divide by maxscores to create finalscore array
    finalscore = [i / j for i, j in zip(individ_scores, y)]
    finalscore1 = []
    #divide finalscores by .2 and round to nearest half star
    for score in finalscore:
        a = score / .2
        b = round(a*2) /2
        finalscore1.append(b) 
   
    methods = []
    added = "_stars"
    #gets functions used in dictlist, adds star title to them
    for entry in dictlist:
        for user, scores in entry.items():
            for method, score in scores.items():
                if method not in methods:
                    methods.append(method+added)
    #appends new method names with star ratings to new dictionary        
    newdict = dict(zip(methods, finalscore1))              
    FinalDict = { userid: newdict}  
    #returns new dictionary
    return(FinalDict)

print(finalscore(dictlist, "bill"))

def curveddatabase(listofdicts):
    curvedscoredict = []
    #for each userid in dictionary list, we perform finalscore on it, and convert scores into curved star ratings
    for entry in listofdicts:
        for user, scores in entry.items():
            x = finalscore(listofdicts, user)
            #append each dictionary item to list
            curvedscoredict.append(x)
    #return dictionary in original dictionary list form, but with ratings curved and turned into star ratings
    return curvedscoredict        

print("-------------------------")
print(dictlist)
print("---------------------------------")

print(curveddatabase(dictlist))

#print(m)                
                
#print(methodlist)  
# 
# What we need now, is a function that parses a database, creates a list of dictionaries from strings and urlIds, then 
# takes the dictionaries and combines them into one giant dictionary list, this will be represented in this case by DictList, 
# as the variable
# 
# we have to store all the scores initially in this database, once the deadline is reached, submissions end, we calculate 
# adjusted scores for each user in the Dictlist, replace old scores with adjusted scores,
#  and update dictlist with curved scores, and send back to backend
# 
# also, we might want to convert the actual numerical scores into stars, which isnt hard at all, just take finalscores 
# for each user, divide by .2, and round to nearest .5

#  

