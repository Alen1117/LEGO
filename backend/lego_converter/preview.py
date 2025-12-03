from PIL import Image
import io
import base64
import numpy as np

def generate_preview(arr: np.ndarray, scale: int = 10) -> str:
    """Genera una imagen preview escalada del array LEGO"""
    h, w, _ = arr.shape
    img = Image.new("RGB", (w*scale, h*scale))
    for y in range(h):
        for x in range(w):
            color = tuple(int(c) for c in arr[y, x])
            block = Image.new("RGB", (scale, scale), color)
            img.paste(block, (x*scale, y*scale))
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")
