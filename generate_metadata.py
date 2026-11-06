import os
import glob
import json

audio_files = sorted(glob.glob("**/*.wav", recursive=True))

if not audio_files:
    print("لم يتم العثور على ملفات .wav داخل المجلد.")
    exit(1)

records = []
for path in audio_files:
    filename = os.path.basename(path)
    # استنتاج المنطقة تلقائياً إذا كان المجلد يحمل اسمها أو وضع قيمة افتراضية
    region = "Sidi Bel Abbès" if "sba" in path.lower() else ("El Bayadh" if "bayadh" in path.lower() else "Algerian West")
    
    records.append({
        "file_name": path,
        "audio": path,
        "transcription": "",  # للتفريغ النصي
        "region": region,
        "dialect": "Western Algerian",
        "language": "ar-DZ"
    })

with open("metadata.jsonl", "w", encoding="utf-8") as f:
    for item in records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"تم إنشاء metadata.jsonl بنجاح لعدد {len(records)} ملفاً صوتياً.")
