from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_pdf_handwriting_recognizer
from app.ocr.text_complexity import evaluate, good_vocab_stars, efficiency_stars, descriptiveness_stars, \
        sentence_length_stars, word_length_stars
from pydantic import BaseModel

router = APIRouter()


class PdfOcrURL(BaseModel):
    url: str
    get_complexity_score: int = 0


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
        return {
            "ocr_text": joined_text,
            "vocab_score": good_vocab_stars(joined_text),
            "efficiency_score": efficiency_stars(joined_text),
            "descriptiveness_score": descriptiveness_stars(joined_text),
            "sentence_length_score": sentence_length_stars(joined_text),
            "word_length_score": word_length_stars(joined_text),
            "complexity_score": evaluate(joined_text)

        }

    else:
        return "url was not set"
