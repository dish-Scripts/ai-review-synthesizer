from flask import Flask, request, jsonify, send_file
from backend.transcriber import transcribe_audio_from_url
from backend.synthesizer import generate_meta_review
from backend.pdf_utils import convert_text_to_pdf
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def health_check():
    return "✅ AI Review Synthesizer Backend is Running!"

@app.route('/transcribe', methods=['POST'])
def transcribe():
    data = request.get_json()
    urls = data.get("urls", [])

    if not urls:
        return jsonify({"error": "No URLs provided"}), 400

    transcripts = []
    for url in urls:
        transcript = transcribe_audio_from_url(url)
        transcripts.append(transcript)

    return jsonify({"transcripts": transcripts})

@app.route('/synthesize', methods=['POST'])
def synthesize():
    data = request.get_json()
    transcripts = data.get("transcripts", [])

    if not transcripts:
        return jsonify({"error": "No transcripts provided"}), 400

    report = generate_meta_review(transcripts)
    return jsonify({"report": report})

@app.route('/generate-pdf', methods=['POST'])
def generate_pdf():
    data = request.get_json()
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    convert_text_to_pdf(text, temp_pdf.name)

    return send_file(temp_pdf.name, as_attachment=True, download_name="meta-review.pdf")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)

