import streamlit as st
import os
import subprocess
from utils.audio_utils import extract_audio
from utils.transcript_utils import generate_transcript
from utils.chunking import chunk_transcript
from utils.vector_store import store_embeddings
from utils.rag_pipeline import retrieve, answer_question, seconds_to_timestamp
from sentence_transformers import SentenceTransformer

# Create necessary directories
os.makedirs("data/uploads", exist_ok=True)
os.makedirs("data/audio", exist_ok=True)
os.makedirs("data/transcripts", exist_ok=True)

# Check if FFmpeg is available
def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

# Add local FFmpeg to PATH if it exists
ffmpeg_local = os.path.join(os.getcwd(), "ffmpeg")
if os.path.exists(ffmpeg_local):
    os.environ['PATH'] = f"{ffmpeg_local};{os.environ['PATH']}"

st.title("🎓 Chat With Your Lecture")

# Check FFmpeg availability
if not check_ffmpeg():
    st.error("❌ FFmpeg not found! Please run the setup script first:")
    st.code("python setup_ffmpeg.py")
    st.stop()

uploaded_file = st.file_uploader("Upload Lecture Video", type=["mp4"])

if uploaded_file:
    # Save uploaded file
    video_path = "data/uploads/video.mp4"
    with open(video_path, "wb") as f:
        f.write(uploaded_file.read())

    st.success("Video uploaded!")
    
    # Extract audio
    audio_path = extract_audio(video_path, "data/audio/audio.wav")
    if audio_path:
        st.info("Extracting transcript...")
        transcript = generate_transcript(audio_path)

        st.success("Transcript generated!")
        st.info(f"📄 Transcript saved to: data/transcripts/")
        
        # Show transcript preview
        with st.expander("📝 View Transcript"):
            st.text(transcript.get('text', 'No text found'))
        
        chunks = chunk_transcript(transcript)
        st.info(f"Created {len(chunks)} chunks")

        model = SentenceTransformer('all-MiniLM-L6-v2')
        index, vectors, texts, chunks = store_embeddings(chunks)

        query = st.text_input("Ask something about the lecture...")
        if query:
            context, matched_chunks = retrieve(query, index, texts, chunks, model)
            answer = answer_question(context, query)
            st.markdown(f"**Answer:** {answer}")
            for chunk in matched_chunks:
                start_time = seconds_to_timestamp(chunk['start'])
                end_time = seconds_to_timestamp(chunk['end'])
                st.markdown(f"⏱️ [{start_time}–{end_time}]")
    else:
        st.error("Failed to extract audio from video")

