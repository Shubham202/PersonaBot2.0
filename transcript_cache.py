import os
import json
from youtube_transcript_api import (
    YouTubeTranscriptApi,
    NoTranscriptFound,
    TranscriptsDisabled,
)

CACHE_DIR = "cached_transcripts"
os.makedirs(CACHE_DIR, exist_ok=True)


def get_cached_transcript_path(video_id):
    return os.path.join(CACHE_DIR, f"{video_id}.json")


def load_cached_transcript(video_id):
    path = get_cached_transcript_path(video_id)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None


def save_transcript_to_cache(video_id, transcript):
    path = get_cached_transcript_path(video_id)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(transcript, f, ensure_ascii=False, indent=2)


def fetch_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["en"])
    except NoTranscriptFound:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=["hi"])
        except Exception as e:
            print(f"❌ Could not get transcript for {video_id} in 'hi': {e}")
            return None
    except TranscriptsDisabled:
        print(f"❌ Transcripts disabled for video {video_id}")
        return None
    except Exception as e:
        print(f"❌ Unknown error with video {video_id}: {e}")
        return None
    return transcript


def get_transcript_text(video_ids):
    combined_text = ""
    for video_id in video_ids:
        cached = load_cached_transcript(video_id)
        if cached:
            transcript = cached
        else:
            transcript = fetch_transcript(video_id)
            if transcript:
                save_transcript_to_cache(video_id, transcript)
            else:
                continue
        text = " ".join([entry["text"] for entry in transcript])
        combined_text += "\n\n" + text[:1000]
    return combined_text
