from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
# from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
# from app.ocr.text_complexity import evaluate, good_vocab_stars, efficiency_stars, descriptiveness_stars, \
#         sentence_length_stars, word_length_stars
from typing import Dict, List
from pydantic import BaseModel, Field

router = APIRouter()


class Matchmaker(BaseModel):
    user_stories = [
        {
            "uuid": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        },
        {
            "uuid": "12322188",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322188/story_5"
        },
        {
            "uuid": "12322189",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322189/story_5"
        },
        {
            "uuid": "12322190",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322190/story_5"
        },
        {
            "uuid": "12322191",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322191/story_5"
        },
        {
            "uuid": "12322192",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322192/story_5"
        },
        {
            "uuid": "12322193",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322193/story_5"
        },
        {
            "uuid": "12322194",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322194/story_5"
        },
        {
            "uuid": "12322195",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322195/story_5"
        },
    ]

    # user_stories: List[Dict["uuid": str, "s3_dir": str]] = Field(..., example=example)


@router.post('/matchmaker')
async def ocr(params: Matchmaker):
    """
    Matchmakes

    ### Request Body

    - `user_stories`: string
        - example:
    [
        {
            "user_id": "12322187",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
        },
        {
            "user_id": "12322188",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322188/story_5"
        },
        {
            "user_id": "12322189",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322189/story_5"
        },
        {
            "user_id": "12322190",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322190/story_5"
        },
        {
            "user_id": "12322191",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322191/story_5"
        },
        {
            "user_id": "12322192",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322192/story_5"
        },
        {
            "user_id": "12322193",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322193/story_5"
        },
        {
            "user_id": "12322194",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322194/story_5"
        },
        {
            "user_id": "12322195",
            "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322195/story_5"
        },
    ]


    ### Response
    - `teams`: list in list
        - example:
        [
            [
                "12322187",
                "12322188",
                "12322189",
                "12322190"
            ]
            [
                "12322191",
                "12322192",
                "12322193",
                "12322194"
            ]
            [
                "12322195"
            ]
        ]
    """

    for player in params.user_stories:
        pass

    return {}
