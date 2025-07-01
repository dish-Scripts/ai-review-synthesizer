# main.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
import ollama

app = FastAPI()

# CORS: Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check route
@app.get("/")
def root():
    return {"message": "✅ AI Review Synthesizer Backend is Running!"}

# POST endpoint for generating meta-review
@app.post("/generate-meta-review")
async def generate_meta_review(request: Request):
    data = await request.json()
    prompt = data.get("prompt")

    if not prompt:
        return {"error": "No prompt provided."}

    def stream_response():
        response = ollama.chat(
            model="gemma:2b",  # or "mistral"
            messages=[{"role": "user", "content": prompt}],
            stream=True
        )
        for chunk in response:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content

    return StreamingResponse(stream_response(), media_type="text/plain")

