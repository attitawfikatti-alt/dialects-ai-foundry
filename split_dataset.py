import json
import random
from collections import defaultdict

# تثبيت البذرة لضمان تكرار نفس النتيجة بدقة
random.seed(42)

with open("metadata.jsonl", "r", encoding="utf-8") as f:
    records = [json.loads(line) for line in f if line.strip()]

# تجميع العينات حسب المنطقة لضمان تمثيل متوازن
by_region = defaultdict(list)
for r in records:
    by_region[r.get("region", "General")].append(r)

train_records = []
test_records = []

for region, items in by_region.items():
    random.shuffle(items)
    split_idx = int(len(items) * 0.8)  # 80% train, 20% test
    
    for item in items[:split_idx]:
        item["split"] = "train"
        train_records.append(item)
        
    for item in items[split_idx:]:
        item["split"] = "test"
        test_records.append(item)

all_records = train_records + test_records

with open("metadata.jsonl", "w", encoding="utf-8") as f:
    for item in all_records:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")

print(f"إجمالي العينات: {len(all_records)}")
print(f"حزمة التدريب (Train): {len(train_records)} عينة")
print(f"حزمة الاختبار (Test):  {len(test_records)} عينة")
