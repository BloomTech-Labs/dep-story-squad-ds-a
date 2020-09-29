from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer
from app.ocr.text_complexity import evaluate
from pydantic import BaseModel

router = APIRouter()


class ImageOcrURL(BaseModel):
    url: str
    get_complexity_score: int = 0


@router.post('/image_ocr_url')
async def ocr(params: ImageOcrURL):
    """
    Handwriting recognizer with google's vision API for images

    ### Request Body

    - `url`: string
    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text`: string, representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.url is not None:
        ocr_text = google_handwriting_recognizer(url=params.url)
        return {
            "ocr_text": ocr_text,
            "complexity_score": -1 if not params.get_complexity_score else evaluate(" ".join(ocr_text))
        }

    else:
        return "url was not set"
