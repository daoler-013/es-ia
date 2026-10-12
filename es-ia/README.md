# 🔍 ¿Es IA? - Detector Forense Real de Contenido Generado por IA

Aplicación web Full-Stack moderna para analizar si una imagen o vídeo corto ha sido generado por Inteligencia Artificial (Deepfakes, modelos de difusión como Stable Diffusion/Flux/Midjourney, GANs, Sora, Runway, etc.) utilizando **procesamiento forense real con visión por computador y análisis de señales**.

---

## 🌟 Características Principales

1. **Motor Forense de Detección Real (`EsIA-ForensicCore v2.0`)**:
   - **Auditoría Criptográfica y Metadatos**:
     - Inspección profunda de fragmentos (*chunks*) PNG para detectar parámetros reales de generación (`parameters`, `prompt`, `workflow`, `Automatic1111`, `ComfyUI`, `Midjourney`, `NovelAI`).
     - Auditoría de etiquetas EXIF de cámaras físicas (`Make`, `Model`, `FNumber`, `ExposureTime`, `ISOSpeedRatings`) para verificar autenticidad óptica.
     - Detección de firmas C2PA / Content Credentials.
   - **Análisis Espectral 2D por Transformada de Fourier (FFT 2D)**:
     - Detección matemática de cuadrículas de remuestreo (*upsampling grid artifacts*) y asimetría azimutal en el dominio frecuencial.
   - **Ruido de Sensor Físico y Grano (PRNU / Laplaciano)**:
     - Evaluación de la presencia de ruido Gaussiano intrínseco de sensores CMOS/CCD frente a parches hiper-suavizados por difusión matemática.
   - **Análisis de Nivel de Error de Compresión (ELA)**:
     - Recompresión diferencial a calidad 90 para contrastar la heterogeneidad de bloques DCT.
   - **Procesamiento de Vídeo Cuadro a Cuadro con OpenCV**:
     - Decodificación y muestreo uniforme de fotogramas.
     - Medición de fluctuaciones de luminancia (*flickering*) y *jitter* de consistencia temporal inter-cuadro (*frame-to-frame warping*).
   - **Descarga Real de Enlaces Remotos**:
     - Si se introduce una URL, el backend descarga de forma segura el archivo binario y lo procesa directamente con el motor forense.

2. **Frontend Moderno, Minimalista y Adaptado a Móviles**:
   - Tema oscuro *Forensic Dark Mode* con efectos de cristal (*Glassmorphism*), acentos neón y transiciones fluidas.
   - **Zona interactiva Drag & Drop**: Admite imágenes (`JPG`, `PNG`, `WEBP`) y vídeos cortos (`MP4`, `WEBM`, `MOV`) hasta 50 MB.
   - **Previsualizador Multimedia**: Muestra la miniatura o reproductor interactivo del archivo cargado.
   - **Animación Láser de Escaneo**: Efecto de haz láser sobre el archivo mientras se extraen las firmas matemáticas.
   - **Medidor Visual Radial (Circular Gauge)**: Animación del porcentaje de probabilidad de IA junto a un veredicto codificado por colores:
     - 🔴 **GENERADO POR IA** (Probabilidad alta)
     - 🟢 **PROBABLEMENTE REAL** (Captura fotográfica auténtica)
     - 🟡 **RESULTADO INCIERTO** (Muestra con compresión alta o ambigua)
   - **Desglose de Indicadores Forenses con Métricas Reales**: Medición de asimetría azimutal en alta frecuencia, varianza de ruido en áreas lisas, coherencia temporal y metadatos.
   - **Barra de Especificaciones Técnicas**: Muestra resolución, formato, ratio espectral y cuadros analizados.
   - **Herramienta para Copiar Informe**: Exporta el dictamen pericial completo al portapapeles con un clic.

---

## 📁 Estructura del Proyecto

```text
es-ia/
├── api/
│   ├── __init__.py
│   └── detector.py            # Motor forense real (FFT 2D, ELA, PRNU, OpenCV, conectores de APIs)
├── public/
│   ├── index.html             # Interfaz semántica con medidor SVG e indicadores
│   ├── styles.css             # Estilos modernos (dark mode, glassmorphism, responsive)
│   └── app.js                 # Drag & drop, preview multimedia, comunicación API y animación
├── server.py                  # Servidor HTTP y API REST (/api/analyze, /api/health)
├── test_endpoints.py          # Suite de pruebas unitarias y forenses
├── test_server_live.py        # Suite de pruebas en vivo por HTTP
├── requirements.txt           # Dependencias científicas (numpy, pillow, opencv-python, requests)
└── README.md                  # Documentación del proyecto
```

---

## 🚀 Cómo Ejecutar y Probar

### 1. Iniciar el Servidor
```powershell
cd "C:\Users\usuario\.gemini\antigravity\scratch\es-ia"
python server.py
```

Abre en tu navegador:
👉 **[http://localhost:8000](http://localhost:8000)**

### 2. Ejecutar Pruebas Automatizadas
Para verificar el funcionamiento del motor forense sobre imágenes y vídeos sintéticos:
```powershell
python test_endpoints.py
```

Para verificar las llamadas HTTP contra el servidor en ejecución:
```powershell
python test_server_live.py
```

---

## 🔌 Conexión con Modelos y APIs Externas

El módulo `api/detector.py` ya incluye los conectores implementados para alternar entre el motor forense local y modelos de aprendizaje profundo en la nube:

### Opción 1: Hugging Face Inference API (Modelo ViT Open-Source)
Utiliza un transformador de visión especializado (`umm-maybe/AI-image-detector`):
```powershell
$env:AI_DETECTION_PROVIDER="HUGGINGFACE"
$env:HUGGINGFACE_API_TOKEN="tu_hf_token_aqui"
python server.py
```

### Opción 2: Hive Moderation (Especializado en Deepfakes y Vídeo)
```powershell
$env:AI_DETECTION_PROVIDER="HIVE"
$env:HIVE_API_KEY="tu_api_key_aqui"
python server.py
```

### Opción 3: Sightengine (Detección de Imágenes Generadas)
```powershell
$env:AI_DETECTION_PROVIDER="SIGHTENGINE"
$env:SIGHTENGINE_API_USER="tu_user"
$env:SIGHTENGINE_API_SECRET="tu_secret"
python server.py
```

---

## 📡 Endpoints de la API

| Método | Ruta | Descripción | Payload |
|---|---|---|---|
| `GET` | `/api/health` | Estado del servicio y versión | Ninguno |
| `POST` | `/api/analyze` | Análisis forense real de imagen o vídeo | `multipart/form-data` con campo `file` o `application/json` con `{ "url": "..." }` |
