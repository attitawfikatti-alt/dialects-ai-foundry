import json
import subprocess
import os

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

unannotated = [r for r in records if not r.get("transcription")]
print(f"المقاطع المتبقية للتفريغ النصي: {len(unannotated)} / {len(records)}")

for idx, item in enumerate(unannotated[:10], start=1):
    path = item["audio"]
    print(f"\n[{idx}/10] تشغيل: {path} | المنطقة: {item.get('region')}")
    
    # تشغيل الصوت عبر mpv في الخلفية
    subprocess.run(["mpv", "--no-video", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    val = input("أدخل النص المنطوق (أو اضغط Enter للتخطي، q للخروج): ").strip()
    if val.lower() == 'q':
        break
    if val:
        item["transcription"] = val

with open("metadata.jsonl", "w", encoding="utf-8") as f:
    for item in records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print("\nتم حفظ التعديلات في metadata.jsonl بنجاح.")
