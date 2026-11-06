#!/usr/bin/env python3
"""
dialects-ai-foundry - Dataset Export & Splitting Tool
Prepares train/validation/test splits and metadata compatible with Hugging Face & ASR pipelines.
"""

import csv
import json
import os
import random
from pathlib import Path

DATA_DIR = Path("data")
MANIFEST_FILE = DATA_DIR / "manifest.jsonl"
EXPORT_DIR = DATA_DIR / "exported"


def load_valid_records():
    """تحميل السجلات والتأكد من وجود الملف الصوتي والنص."""
    if not MANIFEST_FILE.exists():
        print(f"[!] ملف السجلات {MANIFEST_FILE} غير موجود.")
        return []

    valid = []
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                continue

            audio_path = item.get("audio_filepath", "")
            text = item.get("text", "").strip()

            # التحقق من وجود الصوت والتفريغ النصي
            if os.path.exists(audio_path) and text:
                valid.append(item)
            else:
                # إذا كانت العينة تجريبية أو الصوت مفقود يتم تخطيها
                pass

    return valid


def save_split_jsonl(filepath, records):
    with open(filepath, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def save_hf_metadata_csv(filepath, records):
    """توليد ملف metadata.csv المتوافق مع مكتبة Hugging Face datasets."""
    fieldnames = ["file_name", "transcription", "region", "wilaya", "speaker_gender", "speaker_age"]
    with open(filepath, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in records:
            # اسم الملف الصوتي النسبي
            audio_name = Path(r.get("audio_filepath", "")).name
            writer.writerow({
                "file_name": f"audio/{audio_name}",
                "transcription": r.get("text", ""),
                "region": r.get("region", ""),
                "wilaya": r.get("wilaya", ""),
                "speaker_gender": r.get("speaker_gender", ""),
                "speaker_age": r.get("speaker_age", "")
            })


def export_splits(train_ratio=0.8, val_ratio=0.1, seed=42):
    records = load_valid_records()
    total = len(records)

    print("\n=== dialects-ai-foundry: تصدير وتقسيم البيانات ===")
    print(f"• إجمالي العينات الصالحة (صوت + نص): {total}")

    if total == 0:
        print("[!] لا توجد عينات صالحة للتصدير حالياً (تأكد من وجود الملفات الصوتية في data/audio/).")
        return

    # خلط العينات لضمان عشوائية التقسيم
    random.seed(seed)
    shuffled = records.copy()
    random.shuffle(shuffled)

    EXPORT_DIR.mkdir(parents=True, exist_ok=True)

    # حساب الأحجام
    if total < 3:
        # إذا كانت العينات قليلة جداً نضعها في التدريب للاختبار
        train_data = shuffled
        val_data = []
        test_data = []
    else:
        n_train = int(total * train_ratio)
        n_val = int(total * val_ratio)
        train_data = shuffled[:n_train]
        val_data = shuffled[n_train:n_train + n_val]
        test_data = shuffled[n_train + n_val:]

    # حفظ JSONL لكل فئة
    save_split_jsonl(EXPORT_DIR / "train.jsonl", train_data)
    save_split_jsonl(EXPORT_DIR / "val.jsonl", val_data)
    save_split_jsonl(EXPORT_DIR / "test.jsonl", test_data)

    # حفظ metadata.csv لـ Hugging Face
    save_hf_metadata_csv(EXPORT_DIR / "metadata.csv", shuffled)

    print(f"• عينات التدريب (Train)      : {len(train_data)}")
    print(f"• عينات التحقق (Validation)  : {len(val_data)}")
    print(f"• عينات الاختبار (Test)      : {len(test_data)}")
    print(f"\n[✓] تم إنشاء ملفات التصدير بنجاح داخل: {EXPORT_DIR}/")
    print(f"    - train.jsonl / val.jsonl / test.jsonl")
    print(f"    - metadata.csv (Hugging Face Datasets format)\n")


if __name__ == "__main__":
    export_splits()
