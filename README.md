## Project Overview:

Story Squad is an interactive game where children create stories and illustrations, and compete with other children based on their individual scores. There are two main game types: Multiplayer, and Single Player. 

## Data Sources

Due to COPPA compliance, all data scources are private. Contact the project stakeholder for access.


PDF files containing images of stories and illustrations are analyzed using the Google Vision API, which returns a text string. 

The string is analyzed using a variety of metrics, and a score is returned. 

Player's scores are matched up to their nearest neighbors, and teams of 4 are created.

In the event that the number of players is not divisible by 4, bots are added in an even fashion to teams so that all 
teams are teams of 4. 

## Endpoints

Multiplayer Mode:

Input should be in the form of:

Database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        }, {next user_id: 239103913, next s3_dir: next URL}, etc...
    ]

A list of dictionaries should be given using this exact format and the exact key names. From this each URL in the s3_dir folder is run through our Google Image Recognition model, returning a string of text. From this, a text complexity model is run on each string. From this, a new list of nested dictionaries is created in this format:

List_of_dicts:
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

Each user has a series of text complexity scores, 5 different scores to be precise. A series of calculations are performed on each user's scores, and the final outcome is a list of lists, representing multiplayer matchups. The matchups represent
the groups of 4, 2v2 teams will be matched up from the groups of 4 to compete against each other.

The output for this final list of lists is as follows:

Ouput: [['User1', 'User8', 'User4', '_'], ['User 3', 'User 6', 'User 5', '_']'User7', 'User2', 'User9', '_'], etc...]

In the case where users are not divisible by 4, bots will be evenly added to the last few groups to ensure that the teams are even in number. It is important to note that for multiplayer, scores will be stored in the database over several days. Once the submission deadline has ended, the model will run one time, returning the multiplayer output all at once. 

Single Player Mode:

Players who wish to play in single player will receive a series of scores after they submit their writing document.

If they wish to receive their scores in decimal format, the output will be as follows:
Decimal scores range from 0 to 1.
    
    {
        "vocab_length": score,
        "avg_sentence_length": score,
        "efficiency": score,
        "descriptiveness": score,
        "good_vocab": score,
        "evaluate": score
    }


If they wish to receive their scores in star format, the output will be as follows:
Star scores range from 0 to 5 stars, rounded to the nearest half star.
    {
        "vocab_length": star score,
        "avg_sentence_length": star score,
        "efficiency": star score,
        "descriptiveness": star score,
        "good_vocab": star score,
        "evaluate": star score
    }










