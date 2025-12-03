from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import io
from PIL import Image

from .lego_converter.converter import LegoConverter

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

converter = LegoConverter(num_colors=18)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "LEGO Album Builder API",
        "version": "1.0.0"
    }

@app.post("/upload")
async def upload_image(
    file: UploadFile = File(...),
    size: int = Form(32)
):
    if not file.content_type.startswith("image/"):
        raise HTTPException(400, "Solo se permiten imágenes.")

    raw = await file.read()
    image = Image.open(io.BytesIO(raw)).convert("RGB")

    job_id = uuid.uuid4().hex
    ext = Path(file.filename).suffix or ".png"
    dest = UPLOAD_DIR / f"{job_id}{ext}"
    dest.write_bytes(raw)

    lego_data, preview_b64 = converter.process_image(image, size=size)

    return {
        "job_id": job_id,
        "saved_file": dest.name,
        "lego_data": lego_data,
        "lego_preview": f"data:image/png;base64,{preview_b64}"
    }
