from fastapi import APIRouter, HTTPException
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir
from app.ocr.text_complexity import get_text_scores
from pydantic import BaseModel, Field, validator


router = APIRouter()


class ImageOcrS3Dir(BaseModel):
    s3_dir: str = Field(..., example="new_stories_dataset/singleplayer/username_12322186/story_2")
    get_complexity_score: int = Field(..., example=1)


@router.post('/HTR/image/s3_dir', tags=["Handwritten Text Recognition"])
async def image_handwritten_text_recognition_S3_directory(params: ImageOcrS3Dir):
    """
    Handwriting recognizer with google's vision API for
    all .jpg files in a dir

    ### Request Body

    - `s3_dir`: string
        #### The s3 directory of the images that text and complexity scores are needed.

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    ### Response
    - `ocr_text_list`: list, a list of strings representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_dir is not None:
        ocr_text_list = google_handwriting_recognizer_dir(s3_dir=params.s3_dir)
        scores = -1

        if params.get_complexity_score == 1:
            joined_text = " ".join(ocr_text_list)
            scores = get_text_scores(joined_text)

        return {
            "ocr_text_list": ocr_text_list,
            "scores": scores
        }

    else:
        return "s3_dir was not set"
