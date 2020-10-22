from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer
from app.ocr.text_complexity import get_text_scores, get_text_scores_stars
from pydantic import BaseModel, Field, validator
from typing import Dict

router = APIRouter()


class ImageOcrS3Obj(BaseModel):
    s3_obj: str = Field(..., example="Stories Dataset/Transcribed Stories/31--/3101/Photo 3101.jpg")
    get_complexity_score: int = Field(..., example=1)
    star_rating: int = Field(..., example=1)


class ImageOcrS3ObjResponse(BaseModel):
    ocr_text: str = Field(..., example="time there Was a girl named Mary On a Warm through the Wds near her house loved animals Ince apon a Sunnyday Anry Was Wealhing t look for sane critters to take pctures of, She and nadure all her life even thangh She Was anly nine ylars old she think that she is oplna to die soon, she does go to school hut she isn't that Smarti For example Mary Leven though the pie Was not eveA bitten")
    scores: Dict = Field(..., example={
        "vocab_length": 2.5,
        "avg_sentence_length": 5,
        "efficiency": 4.5,
        "descriptiveness": 4.5,
        "good_vocab": 3.5,
        "evaluate": 2.5
    })



@router.post('/HTR/image/s3_obj', tags=["Handwritten Text Recognition"], dependencies=[Depends(verify_token)], response_model=ImageOcrS3ObjResponse)
async def image_handwritten_text_recognition_S3_object(params: ImageOcrS3Obj):
    """
    Handwriting recognizer with google's vision API for PDFs

    ### Request Body

    - `s3_obj`: string
        #### The s3 key of the single image that text and complexity scores are needed.

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    - `star_rating`: int
        #### A number that is only 0 or 1,
        to specify whether to get the text complexity scores as 0-5 star rating
        or 0-1 floats.

    ### Response
    - `ocr_text`: string, representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_obj is not None:
        ocr_text = google_handwriting_recognizer(s3_obj=params.s3_obj)
        scores = -1
        if params.get_complexity_score == 1:
            if params.star_rating == 0:
                scores = get_text_scores(ocr_text)

            elif params.star_rating == 1:
                scores = get_text_scores_stars(ocr_text)

        return {
            "ocr_text": ocr_text,
            "scores": scores
        }

    else:
        return "s3_obj was not set"
