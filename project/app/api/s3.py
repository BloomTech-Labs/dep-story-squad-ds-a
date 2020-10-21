from fastapi import APIRouter
import pandas as pd
import plotly.express as px
import boto3
from starlette.responses import StreamingResponse
import io
from pydantic import BaseModel, Field

router = APIRouter()

client = boto3.client('s3')

s3 = boto3.resource('s3')
bucket = s3.Bucket('training-images-team-a')


class S3(BaseModel):
    s3_obj: str = Field(..., example="Stories Dataset/Transcribed Stories/32--/3203/Photo 3203.jpg")


@router.post('/get_s3_obj/', tags=["S3 Bucket"])
async def s3(params: S3):
    """
    Retreives an s3 jpg image and streams it back.

    ### Request Body

    - `s3_obj`: str
        #### The S3 Object's string
    
    ### Response
    Streamed image
    """
    f = io.BytesIO()
    bucket.download_fileobj(params.s3_obj, f)
    f.seek(0)
    return StreamingResponse(f, media_type="image/jpg",
    headers={'Content-Disposition': 'inline; filename="%s.jpg"' %(object,)})
