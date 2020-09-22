from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer, evaluate
import dotenv


router = APIRouter()
dotenv.load_dotenv()
# st('0.0.0.0', 4444)


@router.post('/ocr')
async def ocr(url: str = None, s3_obj: str = None):
    """
    Make random baseline predictions for classification problem 🔮

    ### Request Body
    - `x1`: positive float
    - `x2`: integer
    - `x3`: string

    ### Response
    - `prediction`: boolean, at random
    - `predict_proba`: float between 0.5 and 1.0, 
    representing the predicted class's probability

    Replace the placeholder docstring and fake predictions with your own model.
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

