from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token
# from remote_pdb import set_trace as st
from app.ocr.google_handwriting_recognition import google_handwriting_recognizer_dir
from app.ocr.text_complexity import get_text_scores, get_text_scores_stars
from pydantic import BaseModel, Field, validator
from typing import List, Dict

router = APIRouter()


class ImageOcrS3Dir(BaseModel):
    s3_dir: str = Field(..., example="new_stories_dataset/singleplayer/username_12322186/story_2")
    get_complexity_score: int = Field(..., example=1)
    star_rating: int = Field(..., example=1)


class ImageOcrS3DirResponse(BaseModel):
    ocr_text_list: List[str] = Field(..., example=[
        "-3205 robati once was aldog named Bob. Bob didn't like potatoes. He ate a lot There of potaitoes. He didrng like potstaes beca.use once a patato named J Benjamin Franklin hit his head Bob was kAosed out for I haur Jo one day Bob went to Potatoland There was one million quards. They but Bob ate them el When he reached the King of y were really strong Pototoland wich was named King Potatohuad,he ate King Potatohead. But that night, King ",
        "3205 Potatahead crauled out of Bobs head mouth I fed so mushy\" King Potatosaid. watLIm barf nowt Everyone laughed at King Potato head, King Potato head made a machine to suck everyone in the world. He pressed the button and sucked and King Potgiahead world except Bobs When Ring Potato went up everyone in the to sleep that night, Bob put King Potatahed in the Potatoland lava pit and pressed the button to make everyone out of the machine "
        ]
    )
    scores: Dict = Field(..., example={
        "vocab_length": 2.5,
        "avg_sentence_length": 5,
        "efficiency": 5,
        "descriptiveness": 2.5,
        "good_vocab": 4.5,
        "evaluate": 2.5
    })


@router.post('/HTR/image/s3_dir', tags=["Handwritten Text Recognition"], dependencies=[Depends(verify_token)], response_model=ImageOcrS3DirResponse)
async def image_handwritten_text_recognition_S3_directory(params: ImageOcrS3Dir):
    """
    Handwriting recognizer with google's vision API for
    all .jpg files in a dir

    ### Request Body

    - `s3_dir`: string
        #### The s3 directory of the images that text and complexity scores are needed.

    - `get_text_complexity`: int
        #### A number that is only 0 or 1, to specify whether to get the text complexity score or no

    - `star_rating`: int
        #### A number that is only 0 or 1,
        to specify whether to get the text complexity scores as 0-5 star rating
        or 0-1 floats.

    ### Response
    - `ocr_text_list`: list, a list of strings representing the recognized text
    - `complexity_score` float: -1 if 'get_text_complexity' is 0, else 0.0 < < 1.0
    """

    if params.s3_dir is not None:
        ocr_text_list = google_handwriting_recognizer_dir(s3_dir=params.s3_dir)
        scores = -1

        if params.get_complexity_score == 1:
            if params.star_rating == 0:
                joined_text = " ".join(ocr_text_list)
                scores = get_text_scores(joined_text)
            elif params.star_rating == 1:
                joined_text = " ".join(ocr_text_list)
                scores = get_text_scores_stars(joined_text)

        return {
            "ocr_text_list": ocr_text_list,
            "scores": scores
        }

    else:
        return "s3_dir was not set"
