from app.ocr.text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length, tokenize
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir, google_handwriting_recognizer    
import numpy as np         
import statistics 


def store(input_str: str,  username: str) -> int:
    '''
    Stores dictionary object after running the string through complexity model...output is dictionary with
    {userID: {score_names: scores}}

    Input:
    string = "Great success. My name is Borat. I have come to America, to find Pamela Anderson, and \
        make her my wife. Very nice!"

    A = store(string, "bill")
    '''
    d = {
        username: {
            "good_vocab": good_vocab(input_str),
            "efficiency": efficiency(input_str),
            "decriptiveness": descriptiveness(input_str),
           "sentence_length": avg_sentence_length(input_str),
            "word_length": vocab_length(input_str)
            }
        }
    return d


def compiler(listofdicts, function) -> []:
    '''
    Takes in list of dictionaries, and function name, returns array of scores for that
    particular function
    '''
    scorelist = []
    for username in listofdicts:
        for scores in username.values():
            for method, score in scores.items():
                if method == function:
                    scorelist.append(score)

    return(scorelist)


def bigcompile(listofdicts):
    '''
    Scrolls through list of dictionaries using compiler method, returns dictionary object 
    with {method_name: [list of scores]} for all method names used in text complexity process
    '''

    bigscorelist = []
    methodlist = []
    #add different methods to methodlist
    for user in listofdicts:
        for scores in user.values():
            for method in scores.keys():
                if method not in methodlist:
                    methodlist.append(method)
    # for each method in the methodlist, compile, and append the lists to 
    # bigscorelist array
    for method in methodlist:
        x = compiler(listofdicts, method)
        bigscorelist.append(x)
    # return a dictionary object with all methods and their corresponding arrays               
    giantdictionary = dict(zip(methodlist, bigscorelist))

    return(giantdictionary)


def maxscorelist(listofdicts):
    '''
    Compiles all lists of scores and their methods, scrolls through all lists, returns one list of max scores for each
    list : [a, b, c, d, e]
    '''
    # arrange dictionary into methods, and arrays of corresponding scores
    x = bigcompile(listofdicts)
    maxscorelist = []
    for scores in x.values():
        score = np.max(scores)
        maxscorelist.append(score)
    # append high score from each corresponding array to maxscore array, return array

    return(maxscorelist)


def finalscore(listofdicts, userid):
    '''
    Scrolls through list of dictionaries, searches for particular userId, matches user's scores up with maximum scores,
    amends users values to reflect percentage of high score, then turns that amended value into a star rating, returns
    dictionary list in same form of original STORE method dictionary, only this time scores are in star values, and methods
    are in star methods
    '''
    max_scores = maxscorelist(listofdicts)

    individ_scores = []

    for entry in listofdicts:
        for user, scores in entry.items():
            if user == userid:
                for method, score in scores.items():
                    individ_scores.append(score)
    # take individual user scores and divide by maxscores to create finalscore array
    finalscore = [i / j for i, j in zip(individ_scores, max_scores)]
    finalscore1 = []
    # divide finalscores by .2 and round to nearest half star
    for score in finalscore:
        a = score / .2
        b = round(a*2) /2
        finalscore1.append(b) 
   
    methods = []
    added = "_stars"
    # gets functions used in dictlist, adds star title to them
    for entry in listofdicts:
        for user, scores in entry.items():
            for method, score in scores.items():
                if method not in methods:
                    methods.append(method+added)
    # appends new method names with star ratings to new dictionary        
    newdict = dict(zip(methods, finalscore1))
    FinalDict = {userid: newdict}
    # returns new dictionary
    return(FinalDict)


def curveddatabase(listofdicts):
    '''
    performs a compilation of the final score method by compiling all individual final scores into a list of dictionaries
    with all user's scores reflecting a curved star score value
    '''

    curvedscoredict = []
    # for each userid in dictionary list, we perform finalscore on it, and convert scores into curved star ratings
    for entry in listofdicts:
        for user, scores in entry.items():
            x = finalscore(listofdicts, user)
            # append each dictionary item to list
            curvedscoredict.append(x)
    # return dictionary in original dictionary list form, but with ratings curved and turned into star ratings
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

    for entry in Database_list:
        for key, value in entry.items():
            if key == "user_id":
                userlist.append(value)
            elif key == "s3_dir":
                dirlist.append(value)
    stringlist = []
    for url in dirlist:
        output_text = google_handwriting_recognizer_dir(url)
        joined_text = ",".join(output_text)
        # appends joined text for each URL in the directory
        stringlist.append(joined_text)
    # stringlist has list of strings, userlist has list of usernames corresponding to those strings,
    # want to run store on those to make dictionary objects
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
    Input:
        database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }, {next user_id: 239103913, next s3_dir: next URL}, etc...
    ]

    Output:
    d = {
        username: {
            "good_vocab": good_vocab score,
            "efficiency": efficiency score,
            "decriptiveness": descriptiveness score,
           "sentence_length": avg_sentence_length score,
            "word_length": vocab_length score
            }
        }
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
    for url in dirlist:
        output_text = google_handwriting_recognizer_dir(url)
        joined_text = ",".join(output_text)
        # appends joined text for each URL in the directory
        stringlist.append(joined_text)
    # stringlist has list of strings, userlist has list of usernames corresponding to those strings,
    # want to run store on those to make dictionary objects
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

def FinalStarDatabase(Database_list):
    '''
    Takes a stored database and adds the user Id as a key and user as a key value pair to the dictionary itself,
    returns list of dictionaries 
    '''
    a = Star_Scores(Database_list)
    
    newdictlist = []
    for entry in a:
        for user, scores in entry.items():
            x = scores
            x['user_id'] = user
            newdictlist.append(x)
    
    return (newdictlist)

def avg_dict(listofdicts):
    '''
    Takes in a list of dictionaries of users and their complexity score ratings,
    returns a dictionary list of methods and the average score of all users for the particular method
    
    Input: 
    d = {
        username: {
            "good_vocab": good_vocab score,
            "efficiency": efficiency score,
            "decriptiveness": descriptiveness score,
           "sentence_length": avg_sentence_length score,
            "word_length": vocab_length score
            }
        }
    Output:
    {'good_vocab': 0.8159067936109293, 'efficiency': 0.9537209802656028, 'decriptiveness': 0.8992303992303994,\
         'sentence_length': 0.587037037037037, 'word_length': 0.6444444444444445}
    
    
    '''

    x = bigcompile(listofdicts)
    methodlist = []
    
    for method in x.keys():
        y = method
        methodlist.append(y)
    score_lists = []
    
    for scores in x.values():
        score_lists.append(scores)
    #list of averages
    mean_lists = []
    #list of standard deviations
    
    for x in score_lists:
        b = sum(x)/len(x)
        mean_lists.append(b)
    
    
    new_dict = dict(zip(methodlist, mean_lists))
      

    return(new_dict)

def std_dict(listofdicts):
    '''
    Takes in a list of dictionaries, compiles a list of scores for each method, 
    returns a list of methods and the standard deviation based on user scores    

    Input: 
    d = {
        username: {
            "good_vocab": good_vocab score,
            "efficiency": efficiency score,
            "decriptiveness": descriptiveness score,
           "sentence_length": avg_sentence_length score,
            "word_length": vocab_length score
            }
        }
    Output:
    {'good_vocab': 0.08048809118628969, 'efficiency': 0.06409450533789401, 'decriptiveness': 0.15798431326261958,\
         'sentence_length': 0.4609288647734532, 'word_length': 0.21140330656044942}
        
    '''
    
    #Get arrays for all different methods
    x = bigcompile(listofdicts)
    methodlist = []
    
    for method in x.keys():
        y = method
        methodlist.append(y)
    score_lists = []
    std_lists = []
    
    for scores in x.values():
        score_lists.append(scores)
    
    for y in score_lists:
        a = np.std(y)
        std_lists.append(a)
    
    new_dict2 = dict(zip(methodlist, std_lists))    

    return new_dict2 

def divide_chunks(l, n): 
    '''
    Divides a list l into separate lists of length n
    '''  
    # looping till length l 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def matchmaker(listofdicts):
    '''
    Takes in list of dictionaries of users and their scores, matches users up to the average score,
    and uses standard deviations of individual scores to return a dictionary with the {user: overall score}
    score is then used in matchmaking process

    Args:
        listofdicts:
        [
            {
                'user_id1': {
                    "good_vocab": good_vocab score,
                    "efficiency": efficiency score,
                    "decriptiveness": descriptiveness score,
                    "sentence_length": avg_sentence_length score,
                    "word_length": vocab_length score
                }
                'user_id2: {...},
            },
        ]

    Output:
        {'bill': -7.063469408392901, 'Kate': -0.33216749504309295 }    
    '''
    avgdict = avg_dict(listofdicts)
    stddict = std_dict(listofdicts)
    
    usernames = []
    differences = []
    methodnames1 = []
    #Create list of functions used in evaluate method
    for entry in listofdicts:
        for scores in entry.values():
            for methodnames in scores.keys():
                if methodnames not in methodnames1:
                    methodnames1.append(methodnames)
    #Create a list of usernames, create list of user's score minus avg score
    for user in listofdicts:
        for names in user.keys():
            usernames.append(names)
        for scores in user.values():
            for method, score in scores.items():
                for function, avg in avgdict.items():
                    if method == function:
                        x = (score-avg)
                        differences.append(x)
    
    
    
    methodlength = len(methodnames1)
    #create new list of lists that divides all scores by number of different scores
    dividedlists = list(divide_chunks(differences, methodlength)) 
     
    dictlist1 = []
    #Since length of each list inside divided list is length of methods,
    #Scroll through giant list of lists, and link up the method names to scores
    # This now represents each individual user's list of scores,
    # representing the difference in their score from the average score for each method 
    for small_list in dividedlists:
        x = dict(zip(methodnames1, small_list))
        dictlist1.append(x)
    
    std_list1 = []
    #Scroll through each list and divide the difference in scores by the corresponding 
    #standard deviation value for each method
    for entry in dictlist1:
        for method, score in entry.items():
            for function, std in stddict.items():
                if method == function:
                    if std != 0:
                        x = (score / std)
                        std_list1.append(x)
                    elif std == 0:
                        std_list1.append(score)    
    #Append these scores to std_list1, divide the list by the length of methods,
    #And now you have individual standard deviation scores for each method for each player
    #when you divide the big list into small segments based on number of methods
    dividedlists2 = list(divide_chunks(std_list1, methodlength)) 
    
    totalz = []
    #scroll through each individual list, sum all the values, append them to a total list
    for small_list2 in dividedlists2:
        summy = sum(small_list2)
        totalz.append(summy)
        
    #now make final dictionary with total values of standard deviations from means, for all methods,
    # and user names, and return the dictionary
    finalscorez = dict(zip(usernames, totalz))
    return(finalscorez)      

def Final_Match(listofdicts):
    '''
    Takes matchmaking dictionary, orders the values, matches users up with the ordered values,
    and divides all users into teams of 4 based on their ordered value. Accounts for remainder 
    by evenly placing bots in groups, while not disturbing the distribution of scores
    
    Input: 
    d = {
        username: {
            "good_vocab": good_vocab(input_str),
            "efficiency": efficiency(input_str),
            "decriptiveness": descriptiveness(input_str),
           "sentence_length": avg_sentence_length(input_str),
            "word_length": vocab_length(input_str)
            }
        }
        
    Output: [['Bruce', 'Bobby', 'Hadi', '_'], ['Jesse', 'Pierre', 'Kate', '_'], ['Franklin', 'Edward', 'bill', '_']]
    


    '''
    teamsize = 4
    
    userscore_dict = matchmaker(listofdicts)
    userscores = userscore_dict.values()
    #Got all values from list of scores, put in valuelist, sort in descending order
    valuelist = []
    for value in userscores:
        valuelist.append(value)
    valuelist.sort(reverse=True)
    
    finalmatch = []
    botvar = "_"
    #scroll through the numbers in valuelist, if the number == a value in the userscore dictionary,
    #append the corresponding key to the finalmatch list       
    for num in valuelist:
        for user, value in userscore_dict.items():
            if num == value:
                finalmatch.append(user)
    
    if len(finalmatch) % teamsize == 3:
        finalmatch.append(botvar)
    
    elif len(finalmatch) % teamsize == 2:
        if len(finalmatch) < 5:
            finalmatch.append(botvar)
            finalmatch.append(botvar)
        elif len(finalmatch) >5:
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            #now swap botvar with list position -5 to insert robot into the last spot in the 
            #2nd list from the end
            finalmatch[-5], finalmatch[-2] = finalmatch[-2], finalmatch[-5]
                    
    elif len(finalmatch) % teamsize == 1:
        if len(finalmatch) < 2:
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            finalmatch.append(botvar)
        elif len(finalmatch) > 4 and len(finalmatch) < 9:
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            #now swap botvar with list position -5 to insert robot into the last spot in the 
            #2nd list from the end
            finalmatch[-5], finalmatch[-3] = finalmatch[-3], finalmatch[-5]
        elif len(finalmatch) > 8:
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            finalmatch.append(botvar)
            #We are manipulating the 3rd and 2nd lists from the end, so that the order of players
            #does not change when we swap robots in from the first list from the end, into the 2nd and 
            #3rd lists from the end
            finalmatch[-9], finalmatch[-8] = finalmatch[-8], finalmatch[-9]
            finalmatch[-9], finalmatch[-7] = finalmatch[-7], finalmatch[-9]
            finalmatch[-9], finalmatch[-6] = finalmatch[-6], finalmatch[-9]
            finalmatch[-9], finalmatch[-3] = finalmatch[-3], finalmatch[-9]
            finalmatch[-2], finalmatch[-5] = finalmatch[-5], finalmatch[-2]
            finalmatch[-2], finalmatch[-4] = finalmatch[-4], finalmatch[-2]

    #Now that the finalmatch list has the correct order of players, with robots included,
    #We divide the list into teams of 4
    finalmatchedlist =  list(divide_chunks(finalmatch, teamsize))  
    
    #Return the final matched up list of lists, with robots included
    return finalmatchedlist
      

def Pipeline(Database_list):
    '''
    Takes Database_list, runs through Scoredatabase function, returns dictionary list
    Runs dictionary list through Final_Match function, returns list of userid's matched up for multiplayer

    Args: 
        Database_list in this format:
        
        database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }, {next user_id: 239103913, next s3_dir: next URL}, etc...
    ]

    Ouput: [['User1', 'User8', 'User3', '_'], ['User4', 'User5', 'User6', '_'], ['User7', 'User2', 'User9', '_']]
    Users matched up by their scores into teams of 4, bots added as '_'
    
    '''
    
    #Create a list of dictionaries by running a list of dictionaries of UserIDs and their URL's through
    #Google image recognizer. Taking those strings and running text complexity on them. Taking those values and their
    #users, and creating a list of dictionaries.
    
    Dictlist = Scoredatabase(Database_list)
    #Compiling all values from this list of dictionaries, finding avg scores, standard deviation of scores,
    #matching up users with their corresponding scores. Ordering the users into a list, and dividing the list into 
    #teams of 4, adding bots if necessary to even out team list.
    
    Finalmatchups = Final_Match(Dictlist)
    #Returning final list of teams, ready for multiplayer
    
    return Finalmatchups     

def Elo_Started(listofdicts):
     
    Matchups = matchmaker(listofdicts)
    Player_List = []
    for player in Matchups.keys():
        Player_List.append(player)

    ELO_Score = [1000] *len(Player_List)
    Ratings_Dict =  dict(zip(Player_List, ELO_Score)) 

    return Ratings_Dict

#def Elo_Adjustments(dict):

    #Take in previous rating dictionary
    #Adjust based on score
    # From backend, need to receive list of players, who they played against, if they won or lost, and the scores
    #{Userid: xxxxxx, Opponents: [x, y, z, etc], win: (yes/no), points: xxxxx}
    # We then take our stored Ratings_Dict, and make adjustments to userid's scores, and resave the Ratings_Dict

    #Scoring:





if __name__ == "__main__":
    
    database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }
    ]
   
    
                    
    actual_dictionary = [
        
            {"user_id": 5204,
            "s3_dir": 'testing_jesse_pipeline/52--/5204',
        },
        {
            "user_id": 5213,
            "s3_dir": 'testing_jesse_pipeline/52--/5213',
        },
        {
            "user_id": 5222,
            "s3_dir": 'testing_jesse_pipeline/52--/5222',
        },
        # {
        #     "user_id": 5209,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5209',
        # },
        # {
        #     "user_id": 5217,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5217',
        # },
        # {
        #     "user_id": 5224,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5224',
        # },
        # {
        #     "user_id": 5227,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5227',
        # },
        # {
        #     "user_id": 5235,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5235',
        # },
        # {
        #     "user_id": 5216,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5216',
        # },
        
    ]
        
    #print(Pipeline(actual_dictionary))
    #abc = Scoredatabase(actual_dictionary)
    
    
   
    
    
    
    
    
    
    
    
  
    





 