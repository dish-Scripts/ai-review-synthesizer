import os
import whisper
import yt_dlp
import tempfile
import uuid
from concurrent.futures import ThreadPoolExecutor

# 🔁 Background batch transcription for local folder
def transcribe_single_audio(file):
    model = whisper.load_model("base")
    audio_path = os.path.join("audios", file)
    result = model.transcribe(audio_path, task="translate")
    transcript_name = file.replace(".mp3", ".txt")
    transcript_path = os.path.join("transcripts", transcript_name)

    os.makedirs("transcripts", exist_ok=True)
    with open(transcript_path, "w", encoding="utf-8") as f:
        f.write(result["text"])
    print(f"✅ Saved transcript: {transcript_path}")

def transcribe_audio():
    files = [f for f in os.listdir("audios") if f.endswith(".mp3")]
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(transcribe_single_audio, files)

# ✅ This is the one used by your backend API
def transcribe_audio_from_url(url):
    output_dir = tempfile.mkdtemp()
    filename = os.path.join(output_dir, f"{uuid.uuid4()}.mp3")

    # Download audio from YouTube
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    # Transcribe with Whisper
    model = whisper.load_model("base")
    result = model.transcribe(filename, task="translate")
    return result["text"]

