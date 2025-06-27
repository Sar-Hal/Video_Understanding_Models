from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles  # ✅ NEW
import os
import time
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-2.5-flash")

# Initialize FastAPI app
app = FastAPI()

# Mount static folder to serve frontend
app.mount("/", StaticFiles(directory="static", html=True), name="static")  # ✅ NEW

# Enable CORS for all origins (adjust in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload video file to Gemini
def upload_video_to_gemini(file_path):
    video_file = genai.upload_file(path=file_path)

    while video_file.state.name == "PROCESSING":
        print("Processing...")
        time.sleep(5)
        video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed")

    return video_file

# Analyze endpoint
@app.post("/analyze_video/")
async def analyze_video(file: UploadFile = File(...), prompt: str = Form(...)):
    file_path = f"temp_{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    try:
        video_file = upload_video_to_gemini(file_path)
        response = MODEL.generate_content([video_file, prompt])
        return JSONResponse(content={"result": response.text})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    finally:
        os.remove(file_path)
