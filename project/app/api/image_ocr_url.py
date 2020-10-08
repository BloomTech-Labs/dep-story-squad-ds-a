from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer
from app.ocr.text_complexity import get_text_scores, get_text_scores_stars
from pydantic import BaseModel, Field, validator

router = APIRouter()


class ImageOcrURL(BaseModel):
    url: str
    get_complexity_score: int = Field(..., example=1)
    star_rating: int = Field(..., example=1)


@router.post('/HTR/image/url', tags=["Handwritten Text Recognition"], dependencies=[Depends(verify_token)])
async def image_handwritten_text_recognition_url(params: ImageOcrURL):
    """
    Handwriting recognizer with google's vision API for images

    ### Request Body

    - `url`: string

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

    if params.url is not None:
        ocr_text = google_handwriting_recognizer(url=params.url)
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
        return "url was not set"
