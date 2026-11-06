#!/usr/bin/env python3
"""
dialects-ai-foundry - Audio & Transcription Review Tool
CLI tool for validating, editing, and tagging dialect dataset samples.
"""

import json
import os
import subprocess
import sys
from pathlib import Path

# مسارات البيانات
DATA_DIR = Path("data")
MANIFEST_FILE = DATA_DIR / "manifest.jsonl"
REVIEWED_FILE = DATA_DIR / "manifest_reviewed.jsonl"


def play_audio(audio_path):
    """تشغيل الصوت داخل Termux عبر termux-api أو مشغلات Linux المتاحة."""
    if not os.path.exists(audio_path):
        print(f"\n[!] الملف الصوتي غير موجود: {audio_path}")
        return

    players = [
        ["termux-media-player", "play", str(audio_path)],
        ["mpv", "--no-video", str(audio_path)],
        ["play", str(audio_path)],
        ["aplay", str(audio_path)],
    ]

    for cmd in players:
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except FileNotFoundError:
            continue

    print("\n[!] لم يتم العثور على مشغل صوتي (ثبت: pkg install termux-api أو mpv)")


def load_manifest(filepath):
    if not filepath.exists():
        print(f"[!] الملف {filepath} غير موجود.")
        sys.exit(1)

    records = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def get_reviewed_ids(filepath):
    if not filepath.exists():
        return set()
    reviewed = set()
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                data = json.loads(line)
                reviewed.add(data.get("id"))
    return reviewed


def append_reviewed(filepath, record):
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def review_loop():
    records = load_manifest(MANIFEST_FILE)
    reviewed_ids = get_reviewed_ids(REVIEWED_FILE)

    pending = [r for r in records if r.get("id") not in reviewed_ids]
    total = len(records)
    done_count = len(reviewed_ids)

    print(f"=== dialects-ai-foundry: مراجعة العينات ===")
    print(f"الإجمالي: {total} | المكتمل: {done_count} | المتبقي: {len(pending)}\n")

    if not pending:
        print("[✓] كل العينات تمت مراجعتها بنجاح!")
        return

    for idx, item in enumerate(pending, 1):
        print("=" * 50)
        print(f"العينة [{idx}/{len(pending)}] - المعرف: {item.get('id')}")
        print(f"الولاية/المنطقة : {item.get('region', 'غير محدد')} | {item.get('wilaya', '')}")
        print(f"المتحدث        : {item.get('speaker_gender', '')} ({item.get('speaker_age', '')} سنة)")
        print(f"التفريغ الحالي  : {item.get('text', '')}")
        print(f"الملف الصوتي   : {item.get('audio_filepath', '')}")
        print("=" * 50)

        audio_path = item.get("audio_filepath", "")
        play_audio(audio_path)

        while True:
            choice = input("\n[P] إعادة استماع | [A] اعتماد | [E] تعديل النص | [R] رفض | [Q] خروج: ").strip().lower()

            if choice == "p":
                play_audio(audio_path)

            elif choice == "a":
                item["status"] = "verified"
                append_reviewed(REVIEWED_FILE, item)
                print("[✓] تم الاعتماد.")
                break

            elif choice == "e":
                new_text = input("أدخل النص المعدل: ").strip()
                if new_text:
                    item["text"] = new_text
                    item["status"] = "verified_edited"
                    append_reviewed(REVIEWED_FILE, item)
                    print("[✓] تم تحديث النص والاعتماد.")
                    break
                else:
                    print("[!] لم يتم إدخال نص جديد.")

            elif choice == "r":
                reason = input("سبب الرفض (ضوضاء / لهجة غير مطابقة / صمت): ").strip()
                item["status"] = "rejected"
                item["reject_reason"] = reason or "unspecified"
                append_reviewed(REVIEWED_FILE, item)
                print("[X] تم استبعاد العينة.")
                break

            elif choice == "q":
                print("\nتم حفظ التقدم. إلى اللقاء!")
                sys.exit(0)

            else:
                print("[!] خيار غير صالح، حاول مجدداً.")


if __name__ == "__main__":
    review_loop()
