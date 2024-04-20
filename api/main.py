from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
# from transcript import fetch_transcript

from youtube_transcript_api import YouTubeTranscriptApi
import re
from youtube_transcript_api.formatters import TextFormatter
import json


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost:3000",
    "http://localhost:8080",
    "http://kirak.ai"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def extract_video_id(url):
    pattern = r'(?:https?://)?(?:www\.)?(?:youtube\.com/(?:(?:watch\?(?:.*&)?v=)|(?:embed/|v/|c/))|youtu\.be/)([^&\n?#]+)'
    match = re.search(pattern, url)
    if match:
        return match.group(1)
    else:
        return None


def fetch_transcript(url):
    try:
        video_id = extract_video_id(url)
        if not video_id:
            print("Invalid URL")
            return None

        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        formatter = TextFormatter()
        text_formatted_transcript = formatter.format_transcript(transcript)
        return json.dumps(text_formatted_transcript)
    except Exception as e:
        print(f"Error: {e}")
        return None


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
