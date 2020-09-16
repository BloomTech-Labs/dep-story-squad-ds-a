from fastapi import APIRouter, HTTPException
import pandas as pd
import plotly.express as px
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer, environment_vars_jsonify
import dotenv


router = APIRouter()
dotenv.load_dotenv()
environment_vars_jsonify()


@router.post('/ocr')
async def ocr(url: str):
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

    ocr_text = google_handwriting_recognizer(url=url)
    return {
        'ocr_text': ocr_text
    }
