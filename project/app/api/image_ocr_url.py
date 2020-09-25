from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
from app.ocr.text_complexity import evaluate
from pydantic import BaseModel
from typing import Optional


router = APIRouter()


@router.post('/image_ocr_url')
async def ocr(url: str = None): 
    """
    Handwriting recognizer with google's vision API for images

    ### Request Body
    #### Only 1 parameter needs to be set
    - `url`: string

    - `s3_obj`: string
        - example:
        "Stories Dataset/Transcribed Stories/31--/3101/Photo 3101.jpg"

    ### Response
    - `ocr_text`: string, representing the recognized text
    """

    if url is not None:
        ocr_text = google_pdf_handwriting_recognizer(url=url)
        return {
            "ocr_text": ocr_text,
            "complexity_score": evaluate(" ".join(ocr_text))
        }

    else:
        return "url is not set"