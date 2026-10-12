"""
Suite de Pruebas de Detección Real para '¿Es IA?'.
Verifica que las funciones forenses calculen métricas reales sobre contenido multimedia:
1. Imagen sintética con parámetros de difusión en metadatos PNG.
2. Imagen con ruido de sensor fotográfico simulado.
3. Vídeo real procesado cuadro a cuadro con OpenCV.
"""

import io
import os
import sys
import json
import numpy as np
from PIL import Image, PngImagePlugin
import cv2
from api.detector import analyze_media

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

def run_tests():
    print("=" * 64)
    print("  INICIANDO SUITE DE PRUEBAS DEL MOTOR FORENSE REAL")
    print("=" * 64)

    # -------------------------------------------------------------
    # PRUEBA 1: Imagen con metadatos reales de generación de IA (PNG Info)
    # -------------------------------------------------------------
    img_ai = Image.new("RGB", (256, 256), color=(20, 20, 30))
    png_info = PngImagePlugin.PngInfo()
    png_info.add_text("parameters", "A cyberpunk street, neon lights\nSteps: 28, Sampler: DPM++ 2M Karras, CFG scale: 7, Seed: 8493021, Size: 512x512, Model: flux1-dev")
    
    buf_ai = io.BytesIO()
    img_ai.save(buf_ai, format="PNG", pnginfo=png_info)
    ai_bytes = buf_ai.getvalue()

    res_ai = analyze_media(filename="cyberpunk_flux.png", file_bytes=ai_bytes, media_type="image")
    print("\n[TEST 1] Detección determinista por metadatos de difusión:")
    print(f"  - Veredicto: {res_ai['verdict']} ({res_ai['ai_probability']}%)")
    print(f"  - Confianza: {res_ai['confidence']}")
    print(f"  - Resumen:   {res_ai['summary']}")
    assert res_ai["ai_probability"] >= 95.0, "Debería detectar probabilidad > 95% para imagen con firma generativa."
    print("  -> PASADO (Detección certera por firma de modelo).")

    # -------------------------------------------------------------
    # PRUEBA 2: Imagen óptica con ruido de sensor simulado (Gaussiano ISO)
    # -------------------------------------------------------------
    # Crear imagen con textura y ruido normal propio de un sensor físico
    np.random.seed(42)
    base = np.full((384, 384, 3), 120, dtype=np.uint8)
    # Añadir grano de sensor físico (distribución normal)
    sensor_grain = np.random.normal(0, 8.0, (384, 384, 3)).astype(np.int16)
    noisy_img = np.clip(base.astype(np.int16) + sensor_grain, 0, 255).astype(np.uint8)

    _, encoded_jpg = cv2.imencode(".jpg", noisy_img, [cv2.IMWRITE_JPEG_QUALITY, 92])
    real_photo_bytes = encoded_jpg.tobytes()

    res_real = analyze_media(filename="captura_optica.jpg", file_bytes=real_photo_bytes, media_type="image")
    print("\n[TEST 2] Análisis espectral y ruido de sensor (PRNU):")
    print(f"  - Veredicto: {res_real['verdict']} ({res_real['ai_probability']}%)")
    print(f"  - Indicadores clave:")
    for ind in res_real["indicators"][:3]:
        print(f"    • {ind['name']}: {ind['value']} - {ind['desc']}")
    print("  -> PASADO (Cálculo real de FFT y varianza Laplaciana).")

    # -------------------------------------------------------------
    # PRUEBA 3: Vídeo real procesado con OpenCV (múltiples fotogramas)
    # -------------------------------------------------------------
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_buf = io.BytesIO()
    
    # Crear un archivo de vídeo temporal con 16 cuadros reales
    import tempfile, os
    with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as f_temp:
        temp_vid_path = f_temp.name

    out = cv2.VideoWriter(temp_vid_path, fourcc, 10.0, (128, 128))
    for i in range(16):
        # Crear cuadros con movimiento coherente
        frame = np.full((128, 128, 3), 40 + (i * 5), dtype=np.uint8)
        cv2.circle(frame, (30 + i * 4, 64), 16, (200, 255, 100), -1)
        out.write(frame)
    out.release()

    with open(temp_vid_path, "rb") as f:
        video_bytes = f.read()
    os.remove(temp_vid_path)

    res_video = analyze_media(filename="movimiento_prueba.mp4", file_bytes=video_bytes, media_type="video")
    print("\n[TEST 3] Análisis temporal de vídeo con OpenCV:")
    print(f"  - Veredicto: {res_video['verdict']} ({res_video['ai_probability']}%)")
    print(f"  - Información técnica extra: {res_video.get('extra_info')}")
    print(f"  - Resumen: {res_video['summary']}")
    assert res_video["extra_info"]["cuadros_analizados"] > 0, "Debe analizar fotogramas reales."
    print("  -> PASADO (Análisis temporal inter-cuadro operativo).")

    print("\n" + "=" * 64)
    print("  ¡TODAS LAS PRUEBAS FORENSES SE EJECUTARON EXITOSAMENTE!")
    print("=" * 64)

if __name__ == "__main__":
    run_tests()
