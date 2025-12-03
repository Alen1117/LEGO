# LEGO Album Builder 🧱

Aplicación web que convierte imágenes en mosaicos de bloques LEGO usando K-Means clustering y paleta de colores LEGO oficial.

## 🚀 Despliegue en Railway

### Paso 1: Preparar el repositorio
```bash
git add .
git commit -m "Preparar para Railway"
git push origin master
```

### Paso 2: Desplegar en Railway
1. Ve a [Railway.app](https://railway.app/)
2. Haz clic en **"Start a New Project"**
3. Selecciona **"Deploy from GitHub repo"**
4. Elige este repositorio: `Alen1117/LEGO`
5. Railway detectará automáticamente que es un proyecto Python
6. Espera a que termine el build (~2-3 minutos)
7. Una vez desplegado, obtendrás una URL pública como: `https://tu-proyecto.up.railway.app`

### Paso 3: Actualizar el Frontend
Edita `frontend/index.html` y cambia la URL del fetch:
```javascript
// Línea ~175, cambiar de:
const res = await fetch("http://127.0.0.1:8000/upload", {

// A tu URL de Railway:
const res = await fetch("https://tu-proyecto.up.railway.app/upload", {
```

### Paso 4: Desplegar el Frontend
Opciones:
- **GitHub Pages**: Sube la carpeta `frontend/` a `gh-pages` branch
- **Netlify**: Arrastra la carpeta `frontend/` a [Netlify Drop](https://app.netlify.com/drop)
- **Vercel**: Importa el repo y configura `frontend/` como root

## 🛠️ Tecnologías
- **Backend**: FastAPI + Uvicorn
- **ML**: scikit-learn (K-Means clustering)
- **Procesamiento**: Pillow, NumPy, scikit-image
- **Frontend**: HTML5 + Vanilla JavaScript

## 📦 Estructura del Proyecto
```
LEGO/
├── backend/
│   ├── main.py                    # API FastAPI
│   └── lego_converter/
│       ├── converter.py           # Clase principal
│       ├── image_processing.py    # Pipeline de procesamiento
│       ├── colors.py              # Paleta LEGO
│       └── preview.py             # Generación de preview
├── frontend/
│   └── index.html                 # UI del cliente
├── requirements.txt               # Dependencias Python
├── Procfile                       # Comando de inicio
├── railway.json                   # Configuración Railway
└── runtime.txt                    # Versión de Python
```

## 🎨 Características
- ✅ Conversión de imagen a bloques LEGO
- ✅ K-Means clustering para reducción de colores
- ✅ Paleta de 40+ colores LEGO reales
- ✅ Preview en base64
- ✅ Tamaños configurables (32x32, 48x48, 64x64)
- ✅ CORS habilitado
- ✅ Listo para producción

## 🔧 Desarrollo Local
```bash
# Activar entorno virtual
.\.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar servidor
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000

# Abrir frontend/index.html en el navegador
```

## 📝 Notas
- El backend se autodespliega en Railway con cada push a master
- La carpeta `uploads/` se crea automáticamente
- Las imágenes se almacenan temporalmente en Railway (se borran al reiniciar)
