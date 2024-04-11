from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
from app.transcript import fetch_transcript
app = FastAPI()

origins = [

    "https://www.kirak.ai/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class URL(BaseModel):
    url: str


@app.post("/fetch-transcript")
async def root(body: URL):
    try:
        response = fetch_transcript(body.url)
        return {"transcript": response}
    except Exception as e:
        logging.error('An error occurred: %s', str(e))
        raise HTTPException(status_code=500, detail="Internal Server Error")
