import json
import random
import re
from pathlib import Path
from collections import defaultdict

MANIFEST_PATH = Path("dataset/manifest.jsonl")
DATASET_DIR = Path("dataset")
TRAIN_PATH = DATASET_DIR / "train.jsonl"
VAL_PATH = DATASET_DIR / "val.jsonl"
VOCAB_PATH = DATASET_DIR / "vocab.json"

def normalize_text(text: str) -> str:
    # إزالة التشكيل والتطويل
    text = re.sub(r'[\u064B-\u0652\u0640]', '', text)
    # توحيد أشكال الألف
    text = re.sub(r'[إأآا]', 'ا', text)
    # توحيد الياء والتاء المربوطة
    text = re.sub(r'ة', 'ه', text)
    text = re.sub(r'ى', 'ي', text)
    # تنظيف المسافات والرموز غير المرغوبة
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def main():
    if not MANIFEST_PATH.exists():
        print(f"[!] لم يتم العثور على {MANIFEST_PATH}")
        return

    records = []
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))

    # تصنيف العينات حسب الولاية للحفاظ على التوزيع الجغرافي
    by_state = defaultdict(list)
    vocab = set()

    for r in records:
        norm_text = normalize_text(r["text"])
        r["normalized_text"] = norm_text
        vocab.update(list(norm_text))
        state_key = r.get("state") or "unknown"
        by_state[state_key].append(r)

    train_set = []
    val_set = []

    # تقسيم عشوائي مثبت (seed) لضمان قابلية إعادة الإنتاج
    random.seed(42)

    for state, items in by_state.items():
        random.shuffle(items)
        # تخصيص 15% للتقييم، بحد أدنى عينة واحدة لكل ولاية إن أمكن
        n_val = max(1, int(len(items) * 0.15)) if len(items) >= 4 else 0
        val_set.extend(items[:n_val])
        train_set.extend(items[n_val:])

    # كتابة ملفات التقسيم
    with open(TRAIN_PATH, "w", encoding="utf-8") as f:
        for item in train_set:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    with open(VAL_PATH, "w", encoding="utf-8") as f:
        for item in val_set:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

    # حفظ معجم الحروف
    vocab_list = sorted(list(vocab))
    vocab_dict = {char: idx for idx, char in enumerate(vocab_list)}
    with open(VOCAB_PATH, "w", encoding="utf-8") as f:
        json.dump(vocab_dict, f, ensure_ascii=False, indent=2)

    print("=" * 50)
    print("📊 تقرير تجهيز وتقسيم البيانات (Data Prep & Splits)")
    print("=" * 50)
    print(f"• إجمالي العينات المعالجة: {len(records)}")
    print(f"• عينات التدريب (Train):     {len(train_set)} ({len(train_set)/len(records)*100:.1f}%)")
    print(f"• عينات التقييم (Validation): {len(val_set)} ({len(val_set)/len(records)*100:.1f}%)")
    print(f"• حجم معجم الحروف الفريدة:  {len(vocab_list)} رمز")
    print(f"\n[✓] تم إنشاء:")
    print(f"  - {TRAIN_PATH}")
    print(f"  - {VAL_PATH}")
    print(f"  - {VOCAB_PATH}")
    print("=" * 50)

if __name__ == "__main__":
    main()
