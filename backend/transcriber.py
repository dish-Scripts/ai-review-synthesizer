# transcriber.py
import os
import whisper
from concurrent.futures import ThreadPoolExecutor

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

