from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer, evaluate
import dotenv
import json


router = APIRouter()
dotenv.load_dotenv()
# st('0.0.0.0', 4444)


@router.post('/ocr')
async def ocr(url: str = None, s3_obj: str = None):
    """
    Handwriting recognizer with google's vision API

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
        ocr_text = google_handwriting_recognizer(url=url)
        return {
            'ocr_text': ocr_text
        }

    elif s3_obj is not None:
        ocr_text = google_handwriting_recognizer(s3_obj=s3_obj)
        return {
            'ocr_text': ocr_text
        }

    else:
        return "No parameters were set!"


@router.post('/text_eval')
async def text_eval(text: str):
    return {
        "score": evaluate(str)
    }


@router.post('/get_json')
async def text_eval():
    return_str = ""
    with open("./key.json") as file_obj:
        return_str = file_obj.read()
    return {
        "key_json_inside": return_str
    }