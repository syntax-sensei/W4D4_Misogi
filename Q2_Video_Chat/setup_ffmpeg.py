import os
import subprocess
import sys
import zipfile
import requests
from pathlib import Path

def download_ffmpeg():
    """Download and setup FFmpeg for Windows"""
    print("Setting up FFmpeg for Windows...")
    
    # FFmpeg download URL (latest release)
    ffmpeg_url = "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/ffmpeg-master-latest-win64-gpl.zip"
    
    # Create temp directory
    temp_dir = Path("temp_ffmpeg")
    temp_dir.mkdir(exist_ok=True)
    
    try:
        # Download FFmpeg
        print("Downloading FFmpeg...")
        response = requests.get(ffmpeg_url, stream=True)
        zip_path = temp_dir / "ffmpeg.zip"
        
        with open(zip_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        # Extract FFmpeg
        print("Extracting FFmpeg...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)
        
        # Find the extracted folder
        extracted_folders = [f for f in temp_dir.iterdir() if f.is_dir() and f.name.startswith('ffmpeg')]
        if not extracted_folders:
            raise Exception("Could not find extracted FFmpeg folder")
        
        ffmpeg_folder = extracted_folders[0]
        
        # Copy FFmpeg executables to project directory
        project_dir = Path.cwd()
        ffmpeg_dir = project_dir / "ffmpeg"
        ffmpeg_dir.mkdir(exist_ok=True)
        
        # Copy ffmpeg.exe, ffprobe.exe, and ffplay.exe
        for exe in ['ffmpeg.exe', 'ffprobe.exe', 'ffplay.exe']:
            src = ffmpeg_folder / "bin" / exe
            dst = ffmpeg_dir / exe
            if src.exists():
                import shutil
                shutil.copy2(src, dst)
                print(f"Copied {exe}")
        
        # Add FFmpeg to PATH for this session
        os.environ['PATH'] = f"{ffmpeg_dir};{os.environ['PATH']}"
        
        print("FFmpeg setup complete!")
        print(f"FFmpeg executables are in: {ffmpeg_dir}")
        print("You can now run your Streamlit app.")
        
    except Exception as e:
        print(f"Error setting up FFmpeg: {e}")
        print("\nManual installation instructions:")
        print("1. Download FFmpeg from: https://ffmpeg.org/download.html")
        print("2. Extract to a folder (e.g., C:\\ffmpeg)")
        print("3. Add the bin folder to your system PATH")
        print("4. Restart your terminal/IDE")
    
    finally:
        # Clean up temp files
        if temp_dir.exists():
            import shutil
            shutil.rmtree(temp_dir)

if __name__ == "__main__":
    download_ffmpeg() 