import json
import re

def clean_arabic_transcript(text):
    if not text:
        return ""
    # إزالة التشكيل والحركات
    tashkeel = re.compile(r'[\u0617-\u061A\u064B-\u0652]')
    text = re.sub(tashkeel, '', text)
    # إزالة التطويل (الكشيدة)
    text = re.sub(r'ـ+', '', text)
    # توحيد أشكال الهمزة والألف المتطرفة
    text = re.sub(r'[إأآا]', 'ا', text)
    text = re.sub(r'ى\b', 'ي', text)
    # إزالة علامات الترقيم والأقواس غير الضرورية
    text = re.sub(r'[،,\.\?!؛:"«»\(\)\[\]]', '', text)
    # توحيد المسافات
    text = re.sub(r'\s+', ' ', text).strip()
    return text

meta_file = "metadata.jsonl"
with open(meta_file, "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

updated = 0
for r in records:
    raw = r.get("transcription", "")
    if raw:
        normalized = clean_arabic_transcript(raw)
        if normalized != raw:
            r["transcription"] = normalized
            updated += 1

with open(meta_file, "w", encoding="utf-8") as f:
    for r in records:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")

print(f"تم تطبيع وتوحيد النصوص لعدد {updated} سجلاً بنجاح.")
