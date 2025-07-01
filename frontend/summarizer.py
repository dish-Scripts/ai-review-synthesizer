# summarizer.py
import os
import ollama
from concurrent.futures import ThreadPoolExecutor

summary_folder = "summaries"
os.makedirs(summary_folder, exist_ok=True)
os.makedirs("audios", exist_ok=True)
os.makedirs("transcripts", exist_ok=True)

def summarize_single_file(file):
    transcript_path = os.path.join("transcripts", file)
    summary_path = os.path.join("summaries", file)
    with open(transcript_path, "r", encoding="utf-8") as f:
        text = f.read()

    prompt = f"""
Summarize this review into 5–6 concise bullet points:

{text}
"""
    response = ollama.chat(
        model="gemma:2b",  # or llama3:8b-instruct
        messages=[{"role": "user", "content": prompt}]
    )

    summary = response["message"]["content"]
    os.makedirs("summaries", exist_ok=True)
    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary)
    print(f"✅ Saved summary: {summary_path}")

def summarize_transcripts():
    files = [f for f in os.listdir("transcripts") if f.endswith(".txt")]
    with ThreadPoolExecutor(max_workers=4) as executor:
        executor.map(summarize_single_file, files)

