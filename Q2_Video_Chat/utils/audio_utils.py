import ffmpeg
import os

def extract_audio(video_path, output_audio_path="data/audio/audio.wav"):
    try:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(output_audio_path), exist_ok=True)
        
        # Extract audio using ffmpeg
        (
            ffmpeg
            .input(video_path)
            .output(output_audio_path, format='wav', acodec='pcm_s16le', ac=1, ar='16000')
            .overwrite_output()
            .run(quiet=True)
        )
        return output_audio_path
    except ffmpeg.Error as e:
        print(f"FFmpeg error: {e}")
        return None
    except Exception as e:
        print(f"Error extracting audio: {e}")
        return None
