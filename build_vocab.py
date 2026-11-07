import json
from collections import Counter

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

words = []
for r in records:
    text = r.get("transcription", "").strip()
    if text:
        words.extend(text.split())

vocab_counter = Counter(words)
print(f"إجمالي الكلمات المنطوقة: {len(words)}")
print(f"حجم القاموس الفريد (Vocabulary Size): {len(vocab_counter)} كلمة فريدة")

print("\nأكثر 15 كلمة تكراراً في الداتا:")
for word, count in vocab_counter.most_common(15):
    print(f"  {word:<15} : {count}")
