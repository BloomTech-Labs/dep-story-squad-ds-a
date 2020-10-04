from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dotenv
from app.api import image_ocr_url, image_ocr_s3_obj, pdf_ocr_url, pdf_ocr_s3_obj, s3, image_ocr_s3_dir

dotenv.load_dotenv()

app = FastAPI(
    title='LABS 26 TEAM A STORY-SQUAD DS API',
    description='Endpoints for doing handwritten-text recognition and text complexity',
    version='0.1',
    docs_url='/',
)


# app.include_router(ocr.router)
app.include_router(s3.router)

app.include_router(pdf_ocr_url.router)
app.include_router(pdf_ocr_s3_obj.router)

app.include_router(image_ocr_url.router)
app.include_router(image_ocr_s3_obj.router)

app.include_router(image_ocr_s3_dir.router)

app.include_router(s3.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

if __name__ == '__main__':
    uvicorn.run(app)
