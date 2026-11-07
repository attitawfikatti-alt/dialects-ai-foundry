import json
import wave
import os
from collections import defaultdict

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

stats = defaultdict(lambda: {"count": 0, "duration": 0.0, "transcribed": 0})
splits = defaultdict(int)

for r in records:
    path = r.get("audio", r.get("file_name", ""))
    region = r.get("region", "Unknown")
    split = r.get("split", "unassigned")
    has_text = bool(r.get("transcription", "").strip())
    
    splits[split] += 1
    stats[region]["count"] += 1
    if has_text:
        stats[region]["transcribed"] += 1
        
    if os.path.exists(path):
        try:
            with wave.open(path, 'rb') as w:
                dur = w.getnframes() / float(w.getframerate())
                stats[region]["duration"] += dur
        except Exception:
            pass

print("=== إحصائيات مجموعة البيانات ===")
print(f"إجمالي العينات: {len(records)}")
print(f"التوزيع: Train = {splits['train']} | Test = {splits['test']}")
print("-" * 55)
print(f"{'المنطقة':<20} | {'العدد':<6} | {'المدة (د)':<10} | {'المفرّغ نصياً':<10}")
print("-" * 55)
for reg, data in sorted(stats.items()):
    dur_min = data['duration'] / 60.0
    print(f"{reg:<20} | {data['count']:<6} | {dur_min:<10.2f} | {data['transcribed']:<10}")
print("-" * 55)
