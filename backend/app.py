from fastapi import FastAPI, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles
from fastapi.responses import StreamingResponse

from traffic_processor import process_video
from frame_detector import detect_frame
# from live_stream import generate_frames, live_stats

import shutil
import os

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Upload folder
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Output folder
OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Serve output videos
app.mount(
    "/outputs",
    StaticFiles(directory="outputs"),
    name="outputs"
)


@app.get("/")
def home():
    return {
        "message": "Smart Traffic Analytics API Running"
    }


@app.post("/upload")
async def upload_video(file: UploadFile = File(...)):
    try:

        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        return {
            "status": "success",
            "filename": file.filename
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/analyze")
def analyze_video(filename: str):

    try:

        video_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )

        if not os.path.exists(video_path):

            return {
                "status": "error",
                "message": "File not found"
            }

        stats = process_video(video_path)

        return {
            "status": "success",
            "message": "Analysis Complete",

            "output": stats["output"],

            "cars": stats["cars"],
            "bikes": stats["bikes"],
            "buses": stats["buses"],
            "trucks": stats["trucks"],

            "traffic_status": stats["traffic_status"],
            "vehicles_per_minute": stats["vehicles_per_minute"],

            "traffic_history": stats["traffic_history"]
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# LIVE CAMERA ROUTES
# =========================

# @app.get("/live_feed")
# def live_feed():

#     return StreamingResponse(
#         generate_frames(),
#         media_type="multipart/x-mixed-replace; boundary=frame"
#     )


# @app.get("/live_stats")
# def get_live_stats():

#     return live_stats


@app.post("/detect_frame")
async def detect_frame_api(
    request: Request
):

    image_bytes = await request.body()

    results = detect_frame(
        image_bytes
    )

    return results


print("APP FILE LOADED SUCCESSFULLY")