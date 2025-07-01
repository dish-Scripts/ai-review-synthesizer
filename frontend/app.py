# app.py
import streamlit as st
import os
from pdf_utils import convert_text_to_pdf
from audio_downloader import download_audio
from transcriber import transcribe_audio
from summarizer import summarize_transcripts
from synthesizer import generate_meta_review

# --- Streamlit page config ---
st.set_page_config(
    layout="wide",
    page_title="AI Review Synthesizer",
    page_icon="🔍"
)

API_URL = "https://ai-review-synthesizer-3.onrender.com"


# --- Custom Styling ---
st.markdown("""
    <style>
        .main {
            background-color: #f5f7fa;
        }
        .stButton>button {
            background-color: #1f77b4;
            color: white;
            border-radius: 8px;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stDownloadButton>button {
            border-radius: 6px;
            border: 1px solid #1f77b4;
        }
        h1, h2, h3 {
            color: #1f77b4;
        }
        .block-container {
            padding: 2rem 3rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.title("🧠 AI Review Synthesizer")
st.sidebar.markdown("Built by Dishaan\n\nSummarizes and synthesizes product reviews from YouTube.")
st.sidebar.markdown("---")
st.sidebar.info("1. Paste video links\n2. Generate summaries\n3. View meta-review\n4. Download your report")

# --- Title ---
st.title("🎯 AI-Powered Meta-Review Generator")
st.markdown("Analyze multiple YouTube reviews and generate a structured, AI-powered summary to help make smart purchase decisions.")

st.markdown("---")

# --- Layout ---
col1, col2 = st.columns([2, 3])  # wider right column for output

with col1:
    st.subheader("🔗 Paste YouTube Video Links")
    video_input = st.text_area(
        "Enter one or more YouTube links (each on a new line):",
        height=150,
        placeholder="https://youtube.com/...\nhttps://youtube.com/...",
        key="link_input"
    )

    if st.button("✨ Synthesize Meta-Review"):
        video_links = video_input.strip().splitlines()
        st.success("✅ Processing started...")

        # Run all steps
        download_audio(video_links)
        transcribe_audio()
        summarize_transcripts()

        st.success("✅ Summarization complete. Synthesizing...")

        st.subheader("📋 Live Meta-Review Output")
        generate_meta_review()

        # Show report
        if os.path.exists("report.txt"):
            with open("report.txt", "r", encoding="utf-8") as f:
                report_content = f.read()
            st.text_area("🧠 Final Meta-Review", report_content, height=400)

        # PDF download
        pdf_file = convert_text_to_pdf(report_content)

        st.download_button(
        label="📄 Download Report as PDF",
        data=pdf_file,
        file_name="meta_review.pdf",
        mime="application/pdf"
     )

with col2:
    st.subheader("📊 How It Works")
    st.markdown("""
    1. 🎥 **Ingest Video** – Extracts audio from YouTube video using `yt-dlp`
    2. 🧠 **Transcribe & Translate** – Converts speech to English text via Whisper
    3. 📝 **Summarize** – Condenses each review into 5–6 bullet points
    4. 🔍 **Synthesize** – Uses LLM to compare all reviews and output:
        - Top features
        - Points of agreement/disagreement
        - Consolidated pros & cons
        - Unique reviewer opinions
    """)

    st.image("https://cdn-icons-png.flaticon.com/512/2784/2784451.png", width=300, caption="Your AI Research Assistant")

st.markdown("---")
st.caption("Built with ❤️ using Python, Whisper, Ollama, and Streamlit.")

