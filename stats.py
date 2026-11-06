#!/usr/bin/env python3
"""
dialects-ai-foundry - Dataset Analytics & Statistics Tool
Calculates audio durations, speaker demographics, and geographical coverage.
"""

import json
import os
import wave
from collections import Counter
from pathlib import Path

DATA_DIR = Path("data")
MANIFEST_FILE = DATA_DIR / "manifest.jsonl"


def get_audio_duration(file_path):
    """حساب مدة ملف WAV بالثواني بدقة."""
    if not os.path.exists(file_path):
        return 0.0
    try:
        with wave.open(str(file_path), "rb") as wf:
            frames = wf.getnframes()
            rate = wf.getframerate()
            if rate > 0:
                return frames / float(rate)
    except Exception:
        pass
    return 0.0


def format_seconds(seconds):
    """تنسيق الثواني إلى ساعات ودقائق وثوانٍ."""
    mins, secs = divmod(seconds, 60)
    hours, mins = divmod(mins, 60)
    if hours > 0:
        return f"{int(hours)} س و {int(mins)} د و {secs:.1f} ث"
    elif mins > 0:
        return f"{int(mins)} د و {secs:.1f} ث"
    else:
        return f"{secs:.1f} ثانية"


def generate_stats():
    if not MANIFEST_FILE.exists():
        print(f"[!] ملف السجلات {MANIFEST_FILE} غير موجود.")
        return

    records = []
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    total_samples = len(records)
    if total_samples == 0:
        print("[!] لا توجد عينات مسجلة بعد في الملف.")
        return

    total_duration = 0.0
    valid_audio_count = 0
    regions = Counter()
    wilayas = Counter()
    genders = Counter()
    ages = []
    word_count = 0

    for item in records:
        audio_path = item.get("audio_filepath", "")
        dur = get_audio_duration(audio_path)
        if dur > 0:
            total_duration += dur
            valid_audio_count += 1

        regions[item.get("region", "غير محدد")] += 1
        wilayas[item.get("wilaya", "غير محدد")] += 1
        genders[item.get("speaker_gender", "غير محدد")] += 1

        age = item.get("speaker_age")
        if isinstance(age, (int, float)):
            ages.append(age)
        elif isinstance(age, str) and age.isdigit():
            ages.append(int(age))

        text = item.get("text", "")
        word_count += len(text.split())

    avg_age = sum(ages) / len(ages) if ages else 0
    avg_duration = total_duration / valid_audio_count if valid_audio_count else 0

    print("\n" + "=" * 55)
    print("      📊 تقرير بيانات مشروع: dialects-ai-foundry")
    print("=" * 55)
    print(f"• إجمالي العينات المسجلة  : {total_samples}")
    print(f"• الملفات الصوتية المتوفرة : {valid_audio_count}")
    print(f"• إجمالي مدة التسجيل      : {format_seconds(total_duration)}")
    print(f"• متوسط طول المقطع       : {avg_duration:.2f} ثانية")
    print(f"• إجمالي عدد الكلمات       : {word_count} كلمة")
    print("-" * 55)
    print("📍 التوزيع الجغرافي:")
    print("  - حسب المناطق : " + ", ".join([f"{k} ({v})" for k, v in regions.items()]))
    print("  - حسب الولايات: " + ", ".join([f"{k} ({v})" for k, v in wilayas.items()]))
    print("-" * 55)
    print("👥 إحصائيات المتحدثين:")
    print("  - الجنس       : " + ", ".join([f"{k} ({v})" for k, v in genders.items()]))
    if ages:
        print(f"  - متوسط العمر : {avg_age:.1f} سنة (الأصغر: {min(ages)} | الأكبر: {max(ages)})")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    generate_stats()
