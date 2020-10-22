## Project Overview:

Story Squad is an interactive game where children create stories and illustrations, and compete with other children. There are two main game types: Multiplayer, and Single Player. 

## Data Sources

Due to COPPA compliance, all data scources are private. Contact the project stakeholder for access.


PDF files containing images of stories and illustrations are analyzed using the Google Vision API, which returns a text string. 

The string is analyzed using a variety of metrics, and a score is returned. 

Player's scores are matched up to their nearest neighbors, and teams of 4 are created.

In the event that the number of players is not divisible by 4, bots are added in an even fashion to teams so that all 
teams are teams of 4. 


## Text Complexity methods

Multiplayer Mode:

Input should be in the form of:
```json
Database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        },
        {
            "next user_id": "239103913",
            "next s3_dir": "next URL"
        },
        "etc..."
    ]
```

A list of dictionaries should be given using this exact format and the exact key names. From this each URL in the s3_dir folder is run through our Google Image Recognition model, returning a string of text. From this, a text complexity model is run on each string. From this, a new list of nested dictionaries is created in this format:

```json
List_of_dicts:
        [
            {
                "user_id1": {
                    "good_vocab": "score",
                    "efficiency": "score",
                    "decriptiveness": "score",
                    "sentence_length": "score",
                    "word_length": "score"
                }
                "next dictionary, etc...",
            },
        ]
```

Each user has a series of text complexity scores, 5 different scores to be precise. A series of calculations are performed on each user's scores, and the final outcome is a list of lists, representing multiplayer matchups. The matchups represent
the groups of 4, 2v2 teams will be matched up from the groups of 4 to compete against each other.

The output for this final list of lists is as follows:

Ouput: 
```json
[["User1", "User8", "User4", "_"], 
["User 3", "User 6", "User 5", "_"],
["User7", "User2", "User9", "_"], "etc..."]
```

In the case where the amount of users is not divisible by 4, bots will be evenly added to the last few groups to ensure that the teams are even in number. It is important to note that for multiplayer, scores will be stored in the database over several days. Once the submission deadline has ended, the model will run one time, returning the multiplayer output all at once. 

Single Player Mode:

Players who wish to play in single player will receive a series of scores after they submit their writing document.

If they wish to receive their scores in decimal format, the output will be as follows:
Decimal scores range from 0 to 1.
```json    
    {
        "vocab_length": "score",
        "avg_sentence_length": "score",
        "efficiency": "score",
        "descriptiveness": "score",
        "good_vocab": "score",
        "evaluate": "score"
    }
```

If they wish to receive their scores in star format, the output will be as follows:
Star scores range from 0 to 5 stars, rounded to the nearest half star.
```json
    {
        "vocab_length": "star score",
        "avg_sentence_length": "star score",
        "efficiency": "star score",
        "descriptiveness": "star score",
        "good_vocab": "star score",
        "evaluate": "star score"
    }
```

## FastAPI Endpoints
# `/HTR/pdf/url`
Feed this a POST request in the shape of json, it's 
looking for 2 fields:
 - `song_id_list:` an array of song id's as strings
 - `recommendation_count:` the requested number of 
```js
{
  "song_id_list":
  [
    "7FGq80cy8juXBCD2nrqdWU",
    "20hsdn8oITBsuWNLhzr5eh"
  ],
  "recommendation_count": 3
	
}
```


Handwriting recognizer with google's vision API for PDFs

Handwriting recognizer with google's vision API for
all .jpg files in a dir

### Request Body

- `s3_dir`: string
    #### The s3 directory of the images that text and complexity scores are needed.

- `get_text_complexity`: int
    #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

- `star_rating`: int
    #### A number that is only 0 or 1,
    to specify whether to get the text complexity scores as 0-5 star rating
    or 0-1 floats.

example:
```json
{
  "s3_dir": "new_stories_dataset/singleplayer/username_12322186/story_2",
  "get_complexity_score": 1,
  "star_rating": 1
}
```

### Response
- `ocr_text_list`: list, a list of strings representing the recognized text
- `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0

example:
```json
{
  "ocr_text_list": [
    "-3205 robati once was aldog named Bob. Bob didn't like potatoes. He ate a lot There of potaitoes. He didrng like potstaes beca.use once a patato named J Benjamin Franklin hit his head Bob was kAosed out for I haur Jo one day Bob went to Potatoland There was one million quards. They but Bob ate them el When he reached the King of y were really strong Pototoland wich was named King Potatohuad,he ate King Potatohead. But that night, King ",
    "-3205 robati once was aldog named Bob. Bob didn't like potatoes. He ate a lot There of potaitoes. He didrng like potstaes beca.use once a patato named J Benjamin Franklin hit his head Bob was kAosed out for I haur Jo one day Bob went to Potatoland There was one million quards. They but Bob ate them el When he reached the King of y were really strong Pototoland wich was named King Potatohuad,he ate King Potatohead. But that night, King "
  ],
  "scores": {
    "vocab_length": 2.5,
    "avg_sentence_length": 5,
    "efficiency": 5,
    "descriptiveness": 2.5,
    "good_vocab": 4.5,
    "evaluate": 2.5
  }
}
```
=======
Multiplayer Mode:

Input should be in the form of:
```json
Database = [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        },
        {
            "next user_id": "239103913",
            "next s3_dir": "next URL"
        },
        "etc..."
    ]
```

A list of dictionaries should be given using this exact format and the exact key names. From this each URL in the s3_dir folder is run through our Google Image Recognition model, returning a string of text. From this, a text complexity model is run on each string. From this, a new list of nested dictionaries is created in this format:

```json
List_of_dicts:
        [
            {
                "user_id1": {
                    "good_vocab": "score",
                    "efficiency": "score",
                    "decriptiveness": "score",
                    "sentence_length": "score",
                    "word_length": "score"
                }
                "next dictionary, etc...",
            },
        ]
```

Each user has a series of text complexity scores, 5 different scores to be precise. A series of calculations are performed on each user's scores, and the final outcome is a list of lists, representing multiplayer matchups. The matchups represent
the groups of 4, 2v2 teams will be matched up from the groups of 4 to compete against each other.

The output for this final list of lists is as follows:

Ouput: 
```json
[["User1", "User8", "User4", "_"], 
["User 3", "User 6", "User 5", "_"],
["User7", "User2", "User9", "_"], "etc..."]
```

In the case where the amount of users is not divisible by 4, bots will be evenly added to the last few groups to ensure that the teams are even in number. It is important to note that for multiplayer, scores will be stored in the database over several days. Once the submission deadline has ended, the model will run one time, returning the multiplayer output all at once. 

Single Player Mode:

Players who wish to play in single player will receive a series of scores after they submit their writing document.

If they wish to receive their scores in decimal format, the output will be as follows:
Decimal scores range from 0 to 1.
```json    
    {
        "vocab_length": "score",
        "avg_sentence_length": "score",
        "efficiency": "score",
        "descriptiveness": "score",
        "good_vocab": "score",
        "evaluate": "score"
    }
```

If they wish to receive their scores in star format, the output will be as follows:
Star scores range from 0 to 5 stars, rounded to the nearest half star.
```json
    {
        "vocab_length": "star score",
        "avg_sentence_length": "star score",
        "efficiency": "star score",
        "descriptiveness": "star score",
        "good_vocab": "star score",
        "evaluate": "star score"
    }
```









