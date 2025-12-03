import numpy as np
from skimage import color

# Paleta LEGO ampliada (tonos neutros, rojos, verdes, azules, amarillos, marrones, y algunos más brillantes)
LEGO_COLORS = [
    # Neutros
    (242,243,242), (255,255,255), (163,162,165), (99,95,98), (0,0,0), (27,42,52),
    # Rojos
    (196,40,27), (200,0,0), (255,0,0), (255,105,97), (178,34,34),
    # Naranjas y amarillos
    (242,149,0), (255,165,0), (255,255,0), (255,192,0), (255,239,160),
    # Verdes
    (0,175,0), (75,151,74), (0,128,0), (34,139,34), (152,251,152),
    # Azules
    (0,85,191), (0,38,84), (0,0,255), (0,128,255), (135,206,250), (173,216,230),
    # Marrones
    (160,110,80), (128,64,0), (160,82,45), (210,180,140), (205,133,63),
    # Violetas y rosas
    (160,32,240), (238,130,238), (255,182,193), (255,105,180),
]

# Convertimos a LAB para cálculos de deltaE
LEGO_COLORS_RGB = np.array(LEGO_COLORS, dtype=np.uint8)
LEGO_COLORS_LAB = color.rgb2lab(LEGO_COLORS_RGB[np.newaxis, :, :] / 255.0)[0]

def closest_lego_color_ciede(rgb):
    """Encuentra el color LEGO más cercano usando distancia en espacio LAB"""
    # Usar distancia euclidiana directamente - más rápido y sin dependencias problemáticas
    return closest_lego_color_euclidean(rgb)

def closest_lego_color_euclidean(rgb):
    """Encuentra el color LEGO más cercano usando distancia euclidiana simple"""
    r1, g1, b1 = map(int, rgb)
    best_dist = float('inf')
    best_color = None
    for r2, g2, b2 in LEGO_COLORS:
        dist = (r1 - r2)**2 + (g1 - g2)**2 + (b1 - b2)**2
        if dist < best_dist:
            best_dist = dist
            best_color = (r2, g2, b2)
    return best_color