from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer
from app.ocr.text_complexity import evaluate, good_vocab_stars, efficiency_stars, descriptiveness_stars, \
        sentence_length_stars, word_length_stars
from pydantic import BaseModel

router = APIRouter()


class ImageOcrS3Obj(BaseModel):
    s3_obj: str
    get_complexity_score: int = 0


@router.post('/image_ocr_s3_obj')
async def ocr(params: ImageOcrS3Obj):
    """
    Handwriting recognizer with google's vision API for PDFs

    ### Request Body

    - `s3_obj`: string
        - example:
        "Stories Dataset/Transcribed Stories/31--/3101/Photo 3101.jpg"

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
            scores = {
                "vocab_score": good_vocab_stars(ocr_text),
                "efficiency_score": efficiency_stars(ocr_text),
                "descriptiveness_score": descriptiveness_stars(ocr_text),
                "sentence_length_score": sentence_length_stars(ocr_text),
                "word_length_score": word_length_stars(ocr_text),
                "complexity_score": evaluate(ocr_text)
            }

        return {
            "ocr_text": ocr_text,
            "scores": scores   
        }

    else:
        return "s3_obj was not set"
