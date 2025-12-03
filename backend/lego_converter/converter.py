from PIL import Image
import numpy as np
from .image_processing import process_image as ip_process_image
from .preview import generate_preview

class LegoConverter:
    def __init__(self, num_colors=18):
        self.num_colors = num_colors
    
    def process_image(self, img: Image.Image, size=32):
        """Usa el pipeline completo"""
        lego_arr = ip_process_image(img, size=size, k=self.num_colors)
        # Generar preview en base64
        preview_b64 = generate_preview(lego_arr)
        
        # Convertir a formato de bloques para el frontend
        lego_data = self._array_to_blocks(lego_arr)
        return lego_data, preview_b64
    
    def _array_to_blocks(self, arr: np.ndarray):
        """Convierte array numpy a formato de bloques"""
        h, w, _ = arr.shape
        blocks = []
        for y in range(h):
            for x in range(w):
                color = arr[y, x]
                blocks.append({
                    "x": int(x),
                    "y": int(y),
                    "color": [int(color[0]), int(color[1]), int(color[2])]
                })
        return {
            "dimensions": [int(w), int(h)],
            "num_blocks": len(blocks),
            "blocks": blocks
        }

