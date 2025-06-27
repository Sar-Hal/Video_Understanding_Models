from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types
import json
from PIL import Image
from IPython.display import display, Markdown, HTML

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)
MODEL_ID = "gemini-2.5-flash"

app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def upload_video_to_gemini(file_path):
    video_file = client.files.upload(file=file_path)

    while video_file.state == "PROCESSING":
        print("Processing...")
        time.sleep(10)
        video_file = client.files.get(name=video_file.name)

    if video_file.state == "FAILED":
        raise ValueError("Video processing failed")

    return video_file

@app.post("/analyze_video/")
async def analyze_video(file: UploadFile = File(...), prompt: str = Form(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        video_file = upload_video_to_gemini(file_path)
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=[video_file, prompt]
        )
        return JSONResponse(content={"result": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(file_path)
