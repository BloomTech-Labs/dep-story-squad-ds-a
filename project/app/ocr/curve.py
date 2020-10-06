from app.ocr.text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir, google_handwriting_recognizer    
import numpy as np         
#from google_handwriting_recognition.py import google_handwriting_recognizer_dir, google_handwriting_recognizer

def store(input_str: str,  username: str) -> int:
    '''
    Stores dictionary object after running the string through complexity model..output is dictionary with
    {userID: {score_names: scores}}
    '''
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
    
    return(scorelist)


def bigcompile(listofdicts):
    '''
    Scrolls through entire list of dictionaries, returns dictionary object with {method_name: [list of scores]}
    for all method names used in text complexity process
    '''

    bigscorelist = []
    methodlist = []
    #add different methods to methodlist
    for user in listofdicts:
        for name, scores in user.items():
            for method, score in scores.items():
                if method not in methodlist:
                    methodlist.append(method)
    #for each method in the methodlist, compile, and append the lists to 
    #bigscorelist array
    for method in methodlist:
        x = compiler(listofdicts, method)
        bigscorelist.append(x)            
    #return a dictionary object with all methods and their corresponding arrays               
    giantdictionary = dict(zip(methodlist, bigscorelist))
    
    return(giantdictionary)
    


def maxscorelist(listofdicts):
    '''
    Compiles all lists of scores and their methods, scrolls through all lists, returns one list of max scores for each
    list : [a, b, c, d, e, f]
    '''
    #arrange dictionary into methods, and arrays of corresponding scores
    x = bigcompile(listofdicts)
    maxscorelist = []
    for method, scores in x.items():
        score = np.max(scores)
        maxscorelist.append(score)
    #append high score from each corresponding array to maxscore array, return array
        
    return(maxscorelist)




def finalscore(listofdicts, userid):
    '''
    Scrolls through list of dictionaries, searches for particular userId, matches user's scores up with maximum scores,
    amends users values to reflect percentage of high score, then turns that amended value into a star rating, returns
    dictionary list in same form of original STORE method dictionary, only this time scores are in star values, and methods
    are in star methods
    '''
    y = maxscorelist(listofdicts)
    
    individ_scores = []
    
    for entry in listofdicts:
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
    for entry in listofdicts:
        for user, scores in entry.items():
            for method, score in scores.items():
                if method not in methods:
                    methods.append(method+added)
    #appends new method names with star ratings to new dictionary        
    newdict = dict(zip(methods, finalscore1))              
    FinalDict = { userid: newdict}  
    #returns new dictionary
    return(FinalDict)



def curveddatabase(listofdicts):
    '''
    performs a compilation of the final score method by compiling all individual final scores into a list of dictionaries
    with all user's scores reflecting a curved star score value
    '''
    
    curvedscoredict = []
    #for each userid in dictionary list, we perform finalscore on it, and convert scores into curved star ratings
    for entry in listofdicts:
        for user, scores in entry.items():
            x = finalscore(listofdicts, user)
            #append each dictionary item to list
            curvedscoredict.append(x)
    #return dictionary in original dictionary list form, but with ratings curved and turned into star ratings
    return curvedscoredict        



def Star_Scores(Database_list):
    '''
    This function does it all. Takes in a Database list, parses it for s3 links, and user IDs, runs google image 
    recognizer on the strings, and implements the Store method on the string:UserId. 
    Compiles all Store dictionaries into one dictionary list, and then runs the curveddatabase function on this list,
    returning a list of dictionaries with curved star scores. 
    '''
    
    dictlist1 = []
    userlist = []
    dirlist = []
    

    for x in Database_list:
        for key, value in x.items():
            if key == "user_id":
                userlist.append(value)
            elif key == "s3_dir":
                dirlist.append(value)
    stringlist = []
    for x in dirlist:
        y = google_handwriting_recognizer_dir(x)
        z = ",".join(y)
       #appends joined text for each URL in the directory
        stringlist.append(z)
    #stringlist has list of strings, userlist has list of usernames corresponding to those strings,
    #want to run store on those to make dictionary objects
    dict1 = dict(zip(stringlist, userlist))

    for string, username in dict1.items():
        x = store(string, username) 
        dictlist1.append(x)   
  
    finaldictionary = curveddatabase(dictlist1)
    return finaldictionary



def Scoredatabase(Database_list):
    '''
    Takes in list of dictionaries with s3 URLs and user IDs, 
    Returns List of dictionaries [{user1}:{evaluate:score, good_vocab:score, efficiency:score, \
                            descriptiveness:score, sentence_length:score, word_length:score}}, {user2}:{etc}}]
    '''

    dictlist1 = []
    userlist = []
    dirlist = []
    

    for x in Database_list:
        for key, value in x.items():
            if key == "user_id":
                userlist.append(value)
            elif key == "s3_dir":
                dirlist.append(value)
    stringlist = []
    for x in dirlist:
        y = google_handwriting_recognizer_dir(x)
        z = ",".join(y)
       #appends joined text for each URL in the directory
        stringlist.append(z)
    #stringlist has list of strings, userlist has list of usernames corresponding to those strings,
    #want to run store on those to make dictionary objects
    dict1 = dict(zip(stringlist, userlist))

    for string, username in dict1.items():
        x = store(string, username) 
        dictlist1.append(x)   

    return dictlist1     

def FinalStoreDatabase(Database_list):
    '''
    Takes a stored database and adds the user Id as a key and user as a key value pair to the dictionary itself,
    returns list of dictionaries 
    '''
    a = Scoredatabase(Database_list)
    
    newdictlist = []
    for entry in a:
        for user, scores in entry.items():
            x = scores
            x['userid'] = user
            newdictlist.append(x)
    
    return (newdictlist)

if __name__ == "__main__":

    string = "Great success. My name is Borat. I have come to America, to find Pamela Anderson, and \
        make her my wife. Very nice!"
    string2 = "take in a database of URLs associated with particular usernames, store it in dictionary with scores,\
    append it to dict_list2, now should have list of dictionaries to scroll through"
    string3 = " Once you have a list of dictionaries, you can scroll through each score related to each function, \
    one by one,  and get the data needed to start implementing the curve function, to then ultimately, \
        return star values for each player"
    string4 = "Remember that the Learning Rate is a hyperparameter that is specific to your gradient-descent based optimizer \
    selection. A learning rate that is too high will cause divergent behavior, but a Learning Rate that is\
         too low will fail to converge, again, you're looking for the sweet spot."
    string5 = "Momentum is a hyperparameter that is more commonly associated with Stochastic Gradient Descent. \
    SGD is a common optimizer because it's what people understand and know, but I doubt it will get you the \
        best results, you can try hyperparameter tuning its attributes and see if you can beat the performance from adam."         
    string6 = "Using dropout on hidden layers might not have any effect while using dropout on hidden layers might\
     have a substantial effect. You don't necessarily need to turn use dropout unless you see that your model\
          has overfitting and generalizability problems."
    string7 = "In the case of a binomial outcome (flipping a coin), the binomial distribution may be \
    approximated by a normal distribution (for sufficiently large n {\displaystyle n} n). Because \
        the square of a standard normal distribution is the chi-square distribution with one degree of freedom,\
             the probability of a result such as 1 heads in 10 trials can be approximated either by using \
                 the normal distribution directly, or the chi-square distribution for the normalised,\
                      squared difference between observed and expected value."
    string8 = "The rabbit-hole went straight on like a tunnel for some way, and then dipped suddenly down, so suddenly\
     that Alice had not a moment to think about stopping herself before she found herself falling down a very deep well. "
    
    a = store(string, "bill" )
    #b = store(string2, "Kate")
    #c = store(string3, "Edward")
    #d = store(string4, "Bobby")
    #e = store(string5, "Hadi")
    #f = store(string6, "Jesse")
    #g = store(string7, "Pierre")
    #h = store(string8, "Bruce")

    #print(a)
    #print(b)
    #print(c)

    dictlist2 = []
    dictlist2.append(a)
    #dictlist2.append(b)
    #dictlist2.append(c)
    #dictlist2.append(d)
    #dictlist2.append(e)
    #dictlist2.append(f)
    #dictlist2.append(g)
    #dictlist2.append(h)

    database =    [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }
        
    ]
    #print("-----------------------")
    #print(compiler(dictlist2, "evaluate")) 
    #print("----------------")
    #x = bigcompile(dictlist2)
    #print(x)
    #print("---------------------------")
    #print(maxscorelist(dictlist2)) 
    #print("-----------------------------")
    #print("-------------------------")
    #print(dictlist2)
    #print("---------------------------------") 
    #print(finalscore(dictlist2, "bill"))
    #print(curveddatabase(dictlist2))

    #print(Star_Scores(database))
    #print(Scoredatabase(database))
    print(dictlist2)
    print(FinalStoreDatabase(database))         
#print(maxscorelist(abc))

#print(bigcompile(create_dictlist(database)))     
#print(a)
#print(b)
# Work with dictlist 2 to make a sample matchmaking model 

 


  

