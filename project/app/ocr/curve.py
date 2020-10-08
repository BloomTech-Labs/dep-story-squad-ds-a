from app.ocr.text_complexity import evaluate, good_vocab, efficiency, descriptiveness, \
        avg_sentence_length, vocab_length
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir, google_handwriting_recognizer    
import numpy as np         
import statistics 


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
           #"sentence_length": avg_sentence_length(input_str),
            "word_length": vocab_length(input_str)
            }
        }
    return d


def compiler(listofdicts, function) -> []:
    '''
    takes in list of dictionaries, and function name, returns array of scores for that
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
    Scrolls through entire list of dictionaries, returns dictionary object with {method_name: [list of scores]}
    for all method names used in text complexity process
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
    list : [a, b, c, d, e, f]
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
    Takes in a list of dictionaries of users and their complexity score ratings , their corresponding methods,
    returns a dictionary list, 1st dictionary represents average of scores, 
    2nd dictionary represents standard deviation of scores
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
    takes in a ist of dictionaries, compiles a list of scores for each method, 
    returns a list of methods and their standard deviations
    '''
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
    '''
    avgdict = avg_dict(listofdicts)
    stddict = std_dict(listofdicts)
    
    usernames = []
    differences = []
    methodnames1 = []
    
    for entry in listofdicts:
        for scores in entry.values():
            for methodnames in scores.keys():
                if methodnames not in methodnames1:
                    methodnames1.append(methodnames)
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
    

    dividedlists = list(divide_chunks(differences, methodlength)) 
     
    dictlist1 = []
    
    for small_list in dividedlists:
        x = dict(zip(methodnames1, small_list))
        dictlist1.append(x)
    
    #we have list of dictionaries with score - avg for each user
    #now we just divide by std list
    #print(len(dictlist4))
    #print(usernames)
    #print(stddict)
    std_list1 = []
    
    for entry in dictlist1:
        for method, score in entry.items():
            for function, std in stddict.items():
                if method == function:
                    if std != 0:
                        x = (score / std)
                        std_list1.append(x)
                    elif std == 0:
                        std_list1.append(score)    
    #print(std_list3)
    dividedlists2 = list(divide_chunks(std_list1, methodlength)) 
    
    totalz = []
    for small_list2 in dividedlists2:
        summy = sum(small_list2)
        totalz.append(summy)
        
    
    finalscorez = dict(zip(usernames, totalz))
    return(finalscorez)      

def Final_Match(listofdicts):
    '''
    Takes matchmaking dictionary, orders the values, matches users up with the ordered values,
    and divides all users into teams of 4 based on their ordered value. Accounts for remainder 
    by evenly placing bots in groups, while not disturbing the distribution of scores
    '''
    teamsize = 4
    
    x = matchmaker(listofdicts)
    y = x.values()
    
    valuelist1 = []
    for value in y:
        valuelist1.append(value)
    valuelist1.sort(reverse=True)
    
    dividedlists= list(divide_chunks(valuelist1, teamsize))
    
    finalmatch = []
    valuelist2 = []
    botvar = "added_cpu_bot"
    
    for lists in dividedlists:
        for value in lists:
            valuelist2.append(value)
    
    for num in valuelist2:
        for user, value in x.items():
            if num == value:
                finalmatch.append(user)
    
    while len(finalmatch) % teamsize != 0:
        if len(finalmatch) % teamsize == 3:
            finalmatch.append(botvar)
        
        elif len(finalmatch) % teamsize == 2:
            if len(finalmatch) < 5:
                finalmatch.append(botvar)
                finalmatch.append(botvar)
            elif len(finalmatch) >5:
                finalmatch.append(botvar)
                finalmatch.append(botvar)
                #now swap botvar with list position -5
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
                finalmatch[-5], finalmatch[-3] = finalmatch[-3], finalmatch[-5]
            elif len(finalmatch) > 8:
                finalmatch.append(botvar)
                finalmatch.append(botvar)
                finalmatch.append(botvar)
                finalmatch[-9], finalmatch[-8] = finalmatch[-8], finalmatch[-9]
                finalmatch[-9], finalmatch[-7] = finalmatch[-7], finalmatch[-9]
                finalmatch[-9], finalmatch[-6] = finalmatch[-6], finalmatch[-9]
                finalmatch[-9], finalmatch[-3] = finalmatch[-3], finalmatch[-9]
                finalmatch[-2], finalmatch[-5] = finalmatch[-5], finalmatch[-2]
                finalmatch[-2], finalmatch[-4] = finalmatch[-4], finalmatch[-2]


    finalmatchedlist =  list(divide_chunks(finalmatch, teamsize))  
    
    return finalmatchedlist
    #return finalmatch  

def Pipeline(Database_list):
    '''
    Takes Database_list, runs through Scoredatabase function, returns dictionary list
    Runs dictionary list through Final_Match function, returns list of userid's matched up for multiplayer
    '''
    
    Dictlist = Scoredatabase(Database_list)
    
    Finalmatchups = Final_Match(Dictlist)

    return Finalmatchups     

#With averages and Standard Deviations of scores, we can now go through individual dictionary entries, compare their individual
# scores to the averages, using standard deviation and absolute value logic, we can give each user an individual +- score,
# for each one of their methods, return eventually an array of users, and their particular overall scores.
# Use that array to match users up with other users, in a manual matchmaking dictionary process.     


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
    string9 = "Tell me that first, and then, if I like being that person,\
         I’ll come up: if not, I’ll stay down here till I’m somebody else’—but, \
             oh dear!” cried Alice, with a sudden burst of tears, “I do wish they\
                  would put their heads down! I am so very tired of being all alone here"

    a = store(string, "bill")
    b = store(string2, "Kate")
    c = store(string3, "Edward")
    d = store(string4, "Bobby")
    e = store(string5, "Hadi")
    f = store(string6, "Jesse")
    g = store(string7, "Pierre")
    h = store(string8, "Bruce")
    i = store(string9, "Franklin")

    # # print(a)
    # # print(b)
    # # print(c)

    dictlist2 = []
    dictlist2.append(a)
    dictlist2.append(b)
    dictlist2.append(c)
    dictlist2.append(d)
    dictlist2.append(e)
    dictlist2.append(f)
    dictlist2.append(g)
    dictlist2.append(h)
    dictlist2.append(i)
    database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }
    ]
    print("####################")
    print(FinalStoreDatabase(database))
    print("####################")
    # print("-----------------------")
    # print(compiler(dictlist2, "evaluate")) 
    # print("----------------")
    # x = bigcompile(dictlist2)
    # print(x)
    # print("---------------------------")
    # print(maxscorelist(dictlist2)) 
    # print("-----------------------------")
    # print("-------------------------")
    # print(dictlist2)
    # print("---------------------------------") 
    # print(finalscore(dictlist2, "bill"))
    # print(curveddatabase(dictlist2))

    # print(Star_Scores(database))
    # print(Scoredatabase(database))
    # print(dictlist2)
    # print(matchmaker(dictlist2))
    
    
    # teamsize = 4
    # x = matchmaker(dictlist2)
    # y = x.values()
    # print(y)
    # valuelist3 = []
    # for value in y:
    #     valuelist3.append(value)
    # valuelist3.sort()
    # print(valuelist3)

    # dividedlists3= list(divide_chunks(valuelist3, teamsize))
    # print(dividedlists3)
    # finalmatch = []
    # valuelist6 = []
    # for lists in dividedlists3:
    #     for value in lists:
    #         valuelist6.append(value)
    # for num in valuelist6:
    #     for key, value in x.items():
    #         if num == value:
    #             finalmatch.append(key)
    # finalmatchedlist =  list(divide_chunks(finalmatch, teamsize))  
    # print(finalmatchedlist)                          
    
    #print(dictlist2)
    print(maxscorelist(dictlist2))
    print(matchmaker(dictlist2))
    print(Final_Match(dictlist2))
    #print(avg_dict(dictlist2))
    #print(std_dict(dictlist2))
    actual_dictionary = [
        # {
        #     "user_id": 5206,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5206',
        # },
        # {
        #     "user_id": 5229,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5229',
        # },
        # {
        #     "user_id": 5210,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5210',
        # },
        # {
        #     "user_id": 5225,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5225',
        # },
        # {
        #     "user_id": 5219,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5219',
        # },
        # {
        #     "user_id": 5208,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5208',
        # },
        # {
        #     "user_id": 5205,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5205',
        # },
        # {
        #     "user_id": 5228,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5228',
        # },
        # {
        #     "user_id": 5232,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5232',
        # },
        # {
        #     "user_id": 5220,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5220',
        # },
        # {
        #     "user_id": 5202,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5202',
        # },
        {
            "user_id": 5230,
            "s3_dir": 'testing_jesse_pipeline/52--/5230',
        },
        {
            "user_id": 5218,
            "s3_dir": 'testing_jesse_pipeline/52--/5218',
        },
        {
            "user_id": 5234,
            "s3_dir": 'testing_jesse_pipeline/52--/5234',
        },
        {
            "user_id": 5214,
            "s3_dir": 'testing_jesse_pipeline/52--/5214',
        },
        {
            "user_id": 5207,
            "s3_dir": 'testing_jesse_pipeline/52--/5207',
        },
        {
            "user_id": 5221,
            "s3_dir": 'testing_jesse_pipeline/52--/5221',
        },
        {
            "user_id": 5204,
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
        # {
        #     "user_id": 5223,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5223',
        # },
        # {
        #     "user_id": 5203,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5203',
        # },
        # {
        #     "user_id": 5215,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5215',
        # },
        # {
        #     "user_id": 5233,
        #     "s3_dir": 'testing_jesse_pipeline/52--/5233'
        # }
    ]
    #actual_dict = [{5206: {'evaluate': 0.386864850604889, 'good_vocab': 0.5025906735751295, 'efficiency': 0.766497461928934, 'decriptiveness': 0.696969696969697, 'sentence_length': 1, 'word_length': 0.4}}, {5229: {'evaluate': 0.37310469710272165, 'good_vocab': 0.3805970149253731, 'efficiency': 0.6323529411764706, 'decriptiveness': 0.6375, 'sentence_length': 1, 'word_length': 0.7}}, {5210: {'evaluate': 0.35023670205895274, 'good_vocab': 0.33986928104575165, 'efficiency': 0.6521739130434783, 'decriptiveness': 0.6704545454545454, 'sentence_length': 1, 'word_length': 0.5}}, {5225: {'evaluate': 0.3042697172108937, 'good_vocab': 0.3247863247863248, 'efficiency': 0.5126050420168067, 'decriptiveness': 0.4805194805194805, 'sentence_length': 1, 'word_length': 0.4}}]
    #print(Final_Match(actual_dict))
    
    #print(Pipeline(actual_dictionary))
    #abc = Scoredatabase(actual_dictionary)
    #print(std_dict(abc))
    #print(std_dict(dictlist2))
    #a = Scoredatabase(actual_dictionary)
    #print(matchmaker(a))
    #print(Pipeline(actual_dictionary))
    


            
    #abc = Scoredatabase(actual_dictionary)
    #print(std_dict(abc))
    #print(dictlist2)
    #print(avg_dict(actual_dict))

    #abc = Scoredatabase(actual_dict2)
    #print(std_dict(dictlist2))
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    #finaldict5 = dict(zip(usernames, dictlist4))
    #finallist3= []
    #finallist3.append(finaldict5)
    #print(finallist3)
    #print(dictlist2)

    





    #need to make userlength many lists from differences and methodnames
    #need to divide differences by userlength increments, and create a dictionary object
    # using methodnames3: differences
    # from there, since they will be ordered, take that dictionary object and attach it to 
    # usernames, 
    # then repeat this process by taking those numbers and dividing them by stddictlist,
    # finally, summing up each 6 values for each participant, to get a final value, 
    # used in matchmaking    


    
    #print(usernames)
         
    


  


# print(bigcompile(create_dictlist(database)))     
# print(a)
# print(b)
# Work with dictlist 2 to make a sample matchmaking model 
