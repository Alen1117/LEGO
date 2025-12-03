import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
from .colors import closest_lego_color_ciede

def resize_to_grid(img: Image.Image, size: int = 32) -> np.ndarray:
    """Redimensiona la imagen a un grid cuadrado."""
    img = img.resize((size, size), Image.LANCZOS)
    return np.array(img)

def reduce_colors_kmeans(arr: np.ndarray, k: int = 18) -> np.ndarray:
    """Reduce los colores usando KMeans."""
    pixels = arr.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=5)
    labels = kmeans.fit_predict(pixels)
    palette = kmeans.cluster_centers_.astype(np.uint8)
    reduced = palette[labels].reshape(arr.shape)
    return reduced

def map_to_lego_colors(arr: np.ndarray, n_colors: int = 18) -> np.ndarray:
    """
    Mapea los colores de la imagen a los más cercanos de LEGO usando clustering.
    """
    # Reducir colores con KMeans
    reduced = reduce_colors_kmeans(arr, k=n_colors)
    h, w, _ = reduced.shape
    pixels = reduced.reshape(-1, 3)

    # Mapear cada cluster a color LEGO
    unique_colors, inverse_idx = np.unique(pixels, axis=0, return_inverse=True)
    lego_palette = np.array([closest_lego_color_ciede(c) for c in unique_colors], dtype=np.uint8)
    lego_pixels = lego_palette[inverse_idx].reshape(h, w, 3)
    
    return lego_pixels
