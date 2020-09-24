from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import dotenv
from app.api import ocr, s3

dotenv.load_dotenv()

app = FastAPI(
    title='LABS 26 TEAM A STORY-SQUAD DS API',
    description='Endpoints for doing handwritten-text recognition and text compexity',
    version='0.1',
    docs_url='/',
)

# app.include_router(viz.router)
# app.include_router(predict.router)
app.include_router(ocr.router)
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
