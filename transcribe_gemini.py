import json
import base64
import requests
import os
import sys

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("خطأ: يرجى تصدير المتغير GEMINI_API_KEY أولاً: export GEMINI_API_KEY='...'")
    sys.exit(1)

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"

pending = [r for r in records if not r.get("transcription", "").strip()]
print(f"المقاطع غير المفرغة: {len(pending)}")

# معالجة أول 5 عينات للتجربة
for idx, item in enumerate(pending[:5], start=1):
    path = item["audio"]
    if not os.path.exists(path):
        continue

    print(f"[{idx}/5] معالجة: {path} ({item.get('region')})...")
    
    with open(path, "rb") as audio_file:
        audio_b64 = base64.b64encode(audio_file.read()).decode("utf-8")

    payload = {
        "contents": [{
            "parts": [
                {"text": "اكتب التفريغ النصي الدقيق لهذا المقطع الصوتي بالدارجة الجزائرية بدون أي شرح إضافي أو تعليق."},
                {"inline_data": {"mime_type": "audio/wav", "data": audio_b64}}
            ]
        }]
    }

    resp = requests.post(url, json=payload)
    if resp.status_code == 200:
        res_json = resp.json()
        try:
            transcription = res_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            item["transcription"] = transcription
            print(f"  -> النتيجة: {transcription}")
        except (KeyError, IndexError):
            print("  -> تعذر استخراج النص.")
    else:
        print(f"  -> خطأ في الاتصال: {resp.status_code}")

with open("metadata.jsonl", "w", encoding="utf-8") as f:
    for item in records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("\nتم حفظ التفريغات الجديدة في metadata.jsonl.")
