import whisper
import json
import os
from datetime import datetime

def generate_transcript(audio_path, save_to_file=True):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path, word_timestamps=True)
    
    if save_to_file:
        # Create transcripts directory if it doesn't exist
        os.makedirs("data/transcripts", exist_ok=True)
        
        # Generate filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        transcript_filename = f"transcript_{timestamp}.json"
        transcript_path = os.path.join("data/transcripts", transcript_filename)
        
        # Save transcript to JSON file
        with open(transcript_path, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        
        print(f"Transcript saved to: {transcript_path}")
    
    return result

def load_transcript(transcript_path):
    """Load a transcript from a JSON file"""
    with open(transcript_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_transcript_text(transcript):
    """Extract just the text from a transcript"""
    return transcript.get('text', '')
