from fastapi import APIRouter
import pandas as pd
import plotly.express as px
import boto3
from starlette.responses import StreamingResponse
import io

router = APIRouter()

client = boto3.client('s3')

s3 = boto3.resource('s3')
bucket = s3.Bucket('training-images-team-a')

@router.get('/s3/{OBJECT}')
async def s3(object):
    f = io.BytesIO()
    client.download_fileobj('training-images-team-a', "Stories Dataset/Transcribed Stories/31--/3101/Photo 3101.jpg", f)
    f.seek(0)
    return StreamingResponse(f, media_type="image/jpg",headers={'Content-Disposition': 'inline; filename="%s.jpg"' %(object,)})
