# backend/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uuid
import io
from PIL import Image
import numpy as np

app = FastAPI()

# Carpeta para guardar uploads
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = (BASE_DIR.parent / "data" / "uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------
# PALETA DE COLORES LEGO
LEGO_COLORS = [
    (242, 243, 242), (27, 42, 52), (163, 162, 165), (99, 95, 98),
    (199, 193, 183), (109, 110, 104), (0, 85, 191), (0, 38, 84),
    (160, 210, 250), (100, 123, 140), (196, 40, 27), (123, 0, 0),
    (198, 141, 155), (253, 131, 172), (215, 197, 153), (160, 140, 90),
    (204, 142, 104), (160, 110, 80), (255, 205, 148), (218, 133, 64),
    (242, 149, 0), (138, 59, 19), (245, 205, 47), (255, 255, 199),
    (202, 176, 0), (75, 151, 74), (0, 69, 26), (0, 175, 0),
    (164, 189, 71), (120, 144, 130), (100, 100, 60), (68, 175, 223),
    (0, 127, 178), (255, 200, 87)
]

# ---------------------------------------------------------
# Funciones auxiliares

def closest_lego_color(rgb):
    r1, g1, b1 = map(int, rgb)  # <-- convierte a int para evitar overflow
    best_dist = float('inf')
    best_color = None
    for r2, g2, b2 in LEGO_COLORS:
        dist = (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2
        if dist < best_dist:
            best_dist = dist
            best_color = (r2, g2, b2)
    return best_color

def map_image_to_lego_palette(image_array):
    """Mapea cada píxel de la imagen a su color LEGO más cercano"""
    h, w, _ = image_array.shape
    lego_array = np.zeros_like(image_array)
    for y in range(h):
        for x in range(w):
            lego_array[y, x] = closest_lego_color(image_array[y, x])
    return lego_array

def median_color(block):
    """Calcula la mediana de todos los píxeles en un bloque"""
    return tuple(np.median(block.reshape(-1, 3), axis=0).astype(int))

def compute_voxel_size(width, height, max_voxel=48):
    """Calcula un tamaño de voxel adaptativo según tamaño de la imagen"""
    return max(1, min(width, height) // max_voxel)

def process_image_to_lego_adaptive(image_bytes, max_voxel=48):
    """Convierte la imagen en bloques LEGO adaptativos estilo mosaico"""
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    arr = np.array(image)
    h, w = arr.shape[:2]

    # Paso 1: mapear toda la imagen a la paleta LEGO
    arr = map_image_to_lego_palette(arr)

    # Paso 2: calcular tamaño de voxel
    voxel_size = compute_voxel_size(w, h, max_voxel)

    lego_blocks = []

    # Paso 3: recorrer bloques
    for y in range(0, h, voxel_size):
        for x in range(0, w, voxel_size):
            block = arr[y:y+voxel_size, x:x+voxel_size]
            color = median_color(block)
            lego_color = closest_lego_color(color)
            lego_blocks.append({
                "x": x // voxel_size,
                "y": y // voxel_size,
                "color": list(lego_color)
            })

    grid_w = (w + voxel_size - 1) // voxel_size
    grid_h = (h + voxel_size - 1) // voxel_size

    return {
        "dimensions": [grid_w, grid_h],
        "num_blocks": len(lego_blocks),
        "blocks": lego_blocks
    }

# ---------------------------------------------------------
# ENDPOINT /upload

@app.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    if not (file.content_type and file.content_type.startswith("image/")):
        raise HTTPException(status_code=400, detail="Only image uploads allowed.")

    job_id = uuid.uuid4().hex
    contents = await file.read()
    if not contents:
        raise HTTPException(status_code=400, detail="Empty upload.")

    # Guardar imagen
    ext = Path(file.filename).suffix or ".png"
    dest_path = UPLOAD_DIR / f"{job_id}{ext}"
    dest_path.write_bytes(contents)

    # Procesar en hilo para no bloquear
    import asyncio
    lego_data = await asyncio.to_thread(process_image_to_lego_adaptive, contents, 48)

    await file.close()

    return {"job_id": job_id, "filename": dest_path.name, "saved": True, "lego_data": lego_data}

# ---------------------------------------------------------
# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
