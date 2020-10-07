from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer
from app.ocr.text_complexity import get_text_scores
from pydantic import BaseModel, Field, validator

router = APIRouter()


class ImageOcrS3Obj(BaseModel):
    s3_obj: str = Field(..., example="Stories Dataset/Transcribed Stories/31--/3101/Photo 3101.jpg")
    get_complexity_score: int = Field(..., example=1)


@router.post('/HTR/image/s3_obj', tags=["Handwritten Text Recognition"], dependencies=[Depends(verify_token)])
async def image_handwritten_text_recognition_S3_object(params: ImageOcrS3Obj):
    """
    Handwriting recognizer with google's vision API for PDFs

    ### Request Body

    - `s3_obj`: string
        #### The s3 key of the single image that text and complexity scores are needed.

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text`: string, representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_obj is not None:
        ocr_text = google_handwriting_recognizer(s3_obj=params.s3_obj)
        scores = -1
        if params.get_complexity_score == 1:
            scores = get_text_scores(ocr_text)

        return {
            "ocr_text": ocr_text,
            "scores": scores
        }

    else:
        return "s3_obj was not set"
