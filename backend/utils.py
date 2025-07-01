# utils.py
import os

def load_all_transcripts(folder="transcripts"):
    """Combine all transcripts into one string for LLM input."""
    combined_text = ""
    for file in sorted(os.listdir(folder)):
        if file.endswith(".txt"):
            path = os.path.join(folder, file)
            with open(path, "r", encoding="utf-8") as f:
                content = f.read().strip()
                combined_text += f"\n### Transcript from {file}:\n{content}\n"
    return combined_text


def save_text(content, filename="report.txt"):
    """Save text content to a file."""
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"📄 Saved file: {filename}")


def clean_text(text):
    """Basic cleanup for LLM outputs (optional usage)."""
    import re
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

