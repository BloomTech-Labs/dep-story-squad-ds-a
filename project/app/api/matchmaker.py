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


# class Matchmaker(BaseModel):
#     user_stories: Dict[str, List] = Field(..., example={
#         "uuids": [
#             "12322187"
#             "12322188"
#             "12322189"
#             "12322190"
#             "12322191"
#             "12322192"
#         ]
#     })


@router.post('/multiplayer/matchmaker', tags=["Multiplayer"], dependencies=[Depends(verify_token)])
async def ocr():
    """
    Matchmakes

    ### Request Body

    - `uuids`: List
        - example:

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

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user_stories')

    database = table.scan()["Items"]

    return Pipeline(database)

