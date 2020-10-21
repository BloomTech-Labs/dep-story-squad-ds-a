from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
# from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
# from app.ocr.text_complexity import evaluate, good_vocab_stars, efficiency_stars, descriptiveness_stars, \
#         sentence_length_stars, word_length_stars
from typing import Dict, List
from pydantic import BaseModel, Field
from app.ocr.curve import Pipeline
import boto3


router = APIRouter()


class MatchmakeResponse(BaseModel):
    user_stories: Dict[str, List] = Field(..., example=[
        [
            "12322187",
            "12322185",
            "12322188",
            "_"
        ],
        [
            "12322189",
            "12322186",
            "_",
            "_"
        ]
    ])


@router.post('/multiplayer/matchmaker', tags=["Multiplayer"], dependencies=[Depends(verify_token)], response_model=MatchmakeResponse)
async def ocr():
    """
    Creates teams of 4, for the multiplayer mode.
    If the number of players is not divisable by 4, it will add at most 3 bots ( "_" ) to some of the teams.
    """

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user_stories')

    database = table.scan()["Items"]

    return Pipeline(database)

