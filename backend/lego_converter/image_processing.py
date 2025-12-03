import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from .colors import closest_lego_color_ciede  # 🔹 usar la función mejorada
from skimage import color

def resize_to_grid(img: Image.Image, size: int = 32) -> np.ndarray:
    """Redimensiona la imagen a un tamaño fijo"""
    img = img.resize((size, size), Image.LANCZOS)  # 🔹 mejor preserva detalles que NEAREST
    return np.array(img)

def reduce_colors_kmeans(arr: np.ndarray, k: int = 18) -> np.ndarray:
    """Reduce la imagen a k colores usando KMeans"""
    pixels = arr.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=5)
    labels = kmeans.fit_predict(pixels)
    palette = kmeans.cluster_centers_.astype(np.uint8)
    reduced = palette[labels].reshape(arr.shape)
    return reduced

def map_to_lego_colors(arr: np.ndarray) -> np.ndarray:
    """Convierte cada píxel al color LEGO más cercano"""
    h, w, _ = arr.shape
    lego_arr = np.zeros_like(arr)
    for y in range(h):
        for x in range(w):
            lego_arr[y, x] = closest_lego_color_ciede(arr[y, x])
    return lego_arr

def process_image(img: Image.Image, size: int = 32, k: int = 18) -> np.ndarray:
    """Pipeline completo: resize -> KMeans -> LEGO colors"""
    arr = resize_to_grid(img, size)
    arr = reduce_colors_kmeans(arr, k=k)
    lego_arr = map_to_lego_colors(arr)
    return lego_arr
