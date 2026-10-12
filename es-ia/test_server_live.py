import urllib.request
import json
import io
from PIL import Image

# 1. Health check
res = urllib.request.urlopen("http://localhost:8000/api/health")
print("Health status:", res.status, res.read().decode())

# 2. Test JSON analyze with remote URL
req_json = urllib.request.Request(
    "http://localhost:8000/api/analyze",
    data=json.dumps({"url": "https://images.unsplash.com/photo-1544005313-94ddf0286df2"}).encode("utf-8"),
    headers={"Content-Type": "application/json"}
)
res_json = urllib.request.urlopen(req_json)
data_json = json.loads(res_json.read().decode("utf-8"))
print("\nAnalyze URL response:")
print("  - Veredicto:", data_json.get("verdict"), f"({data_json.get('ai_probability')}%)")
print("  - Motor:", data_json.get("engine_version"))
print("  - Especificaciones:", data_json.get("extra_info"))
print("  - Resumen:", data_json.get("summary"))

# 3. Test Multipart upload with real generated image
img = Image.new("RGB", (256, 256), color=(80, 120, 160))
buf = io.BytesIO()
img.save(buf, format="JPEG", quality=90)
raw_bytes = buf.getvalue()

boundary = "----TestBoundary987654321"
body = (
    f"--{boundary}\r\n"
    f'Content-Disposition: form-data; name="file"; filename="foto_test.jpg"\r\n'
    f"Content-Type: image/jpeg\r\n\r\n"
).encode("latin-1") + raw_bytes + f"\r\n--{boundary}--\r\n".encode("latin-1")

req_multi = urllib.request.Request(
    "http://localhost:8000/api/analyze",
    data=body,
    headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
)
res_multi = urllib.request.urlopen(req_multi)
data_multi = json.loads(res_multi.read().decode("utf-8"))
print("\nAnalyze Multipart response:")
print("  - Veredicto:", data_multi.get("verdict"), f"({data_multi.get('ai_probability')}%)")
print("  - Motor:", data_multi.get("engine_version"))
print("  - Especificaciones:", data_multi.get("extra_info"))
print("  - Indicadores:", len(data_multi.get("indicators", [])))
print("\n¡TODAS LAS PRUEBAS EN VIVO SOBRE EL SERVIDOR PASARON!")
