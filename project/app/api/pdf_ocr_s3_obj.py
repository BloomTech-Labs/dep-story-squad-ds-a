from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
from app.ocr.text_complexity import get_text_scores
from pydantic import BaseModel, Field, validator

router = APIRouter()


class PdfOcrS3Obj(BaseModel):
    s3_obj: str
    get_complexity_score: int = Field(..., example=1)


@router.post('/HTR/pdf/s3_obj', tags=["Handwritten Text Recognition"], dependencies=[Depends(verify_token)])
async def pdf_handwritten_text_recognition_S3_object(params: PdfOcrS3Obj):
    """
    Handwriting recognizer with google's vision API for PDFs

    ### Request Body

    - `s3_obj`: string

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text`: string, representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_obj is not None:
        ocr_text = google_pdf_handwriting_recognizer(s3_obj=params.s3_obj)
        joined_text = " ".join(ocr_text)
        scores = -1

        if params.get_complexity_score == 1:
            scores = get_text_scores(joined_text)

        return {
            "ocr_text": ocr_text,
            "scores": scores
        }

    else:
        return "s3_obj was not set"
