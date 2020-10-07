from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
from app.ocr.text_complexity import get_text_scores
from pydantic import BaseModel, Field, validator

router = APIRouter()


class PdfOcrURL(BaseModel):
    url: str
    get_complexity_score: int = Field(..., example=1)


@router.post('/HTR/pdf/url', tags=["Handwritten Text Recognition"])
async def pdf_handwritten_text_recognition_url(params: PdfOcrURL):
    """
    Handwriting recognizer with google's vision API for PDFs

    ### Request Body

    - `url`: string

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text`: string, representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.url is not None:
        ocr_text = google_pdf_handwriting_recognizer(url=params.url)
        joined_text = " ".join(ocr_text)
        if params.get_complexity_score == 1:
            scores = get_text_scores(joined_text)

        return {
            "ocr_text": ocr_text,
            "scores": scores   
        }

    else:
        return "url was not set"
