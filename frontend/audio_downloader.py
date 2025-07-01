# audio_downloader.py
import os
import yt_dlp
from concurrent.futures import ThreadPoolExecutor

def download_single_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audios/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def download_audio(video_urls):
    os.makedirs("audios", exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(download_single_audio, video_urls)

