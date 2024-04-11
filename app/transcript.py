from youtube_transcript_api import YouTubeTranscriptApi
import re
from youtube_transcript_api.formatters import TextFormatter
import json


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
