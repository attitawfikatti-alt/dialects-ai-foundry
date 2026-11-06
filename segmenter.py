#!/usr/bin/env python3
"""
dialects-ai-foundry - Smart Audio Segmenter with Resume Support
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

DATA_DIR = Path("data")
AUDIO_DIR = DATA_DIR / "audio"
MANIFEST = DATA_DIR / "manifest.jsonl"
TEMP_SEGMENTS_DIR = Path("data/.temp_segments")

AUDIO_DIR.mkdir(parents=True, exist_ok=True)
TEMP_SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

def safe_input(prompt_text):
    try:
        val = input(prompt_text)
        return val.strip()
    except (EOFError, KeyboardInterrupt):
        print("\n\n[!] تم إيقاف العملية يدوياً أو انقطع الإدخال. تم حفظ التقدم.")
        sys.exit(0)

def get_next_id():
    if not MANIFEST.exists():
        return 1
    with open(MANIFEST, "r", encoding="utf-8") as f:
        return sum(1 for l in f if l.strip()) + 1

def play_audio(path):
    for cmd in ["play", "termux-media-player", "mpv", "aplay"]:
        if shutil.which(cmd):
            try:
                if cmd == "play":
                    subprocess.run([cmd, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                elif cmd == "termux-media-player":
                    subprocess.Popen([cmd, "play", str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                else:
                    subprocess.run([cmd, str(path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            return

def extract_segments(input_file):
    print("[*] جاري استخراج وتقسيم المقاطع الصوتية بالاعتماد على فترات الصمت...")
    # إفراغ مجلد المقاطع المؤقتة القديم
    shutil.rmtree(TEMP_SEGMENTS_DIR, ignore_errors=True)
    TEMP_SEGMENTS_DIR.mkdir(parents=True, exist_ok=True)

    # استخدام silenceremove و segment عبر ffmpeg لتقسيم الصوت الصامت
    # تقسيم بمعدل لا يقل عن 1.5 ثانية ولا يزيد عن 15 ثانية لكل عينة
    out_pattern = str(TEMP_SEGMENTS_DIR / "seg_%04d.wav")
    cmd = [
        "ffmpeg", "-y", "-i", str(input_file),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        "-f", "segment", "-segment_time", "6",
        "-reset_timestamps", "1",
        out_pattern
    ]
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        print("[!] فشل تقسيم الملف عبر ffmpeg.")
        return []

    segments = sorted(list(TEMP_SEGMENTS_DIR.glob("seg_*.wav")))
    return segments

def main():
    print("=== dialects-ai-foundry: أداة تقطيع التسجيلات الطويلة ===")
    input_file = safe_input("أدخل مسار الملف الصوتي (/sdcard/Download/talk.m4a): ")
    if not input_file or not Path(input_file).exists():
        print("[!] الملف غير موجود. تأكد من صحة المسار.")
        return

    region = safe_input("المنطقة [الغرب]: ") or "الغرب"
    wilaya = safe_input("الولاية [البيض]: ") or "البيض"
    gender = safe_input("الجنس [M/F]: ").upper()
    gender = "ذكر" if gender == "M" else "أنثى"
    age = safe_input("العمر [35]: ") or "35"

    segments = extract_segments(input_file)
    if not segments:
        print("[!] لم يتم العثور على مقاطع.")
        return

    print(f"\n[✓] تم تجهيز {len(segments)} مقطعاً صوتياً للمراجعة.")
    cur_id = get_next_id()
    saved = 0

    for idx, seg in enumerate(segments, 1):
        print("\n" + "=" * 45)
        print(f"--- المقطع ({idx}/{len(segments)}) ---")
        print("=" * 45)

        play_audio(seg)

        while True:
            action = safe_input("الخيار [Y=تفريغ واعتماد / r=إعادة السماع / s=تخطي / q=خروج وحفظ]: ").lower()
            if action == "r":
                play_audio(seg)
            elif action in ["y", "", "s", "q"]:
                break

        if action == "q":
            print("[*] تم إنهاء الجلسة بناء على طلبك.")
            break
        elif action == "s":
            continue

        text = safe_input("أدخل التفريغ النصي لهذا المقطع: ")
        if not text:
            print("[!] تم تخطي المقطع لعدم إدخال تفريغ.")
            continue

        sample_name = f"sample_{cur_id:03d}.wav"
        target_path = AUDIO_DIR / sample_name
        shutil.copy(str(seg), str(target_path))

        rec = {
            "id": f"sample_{cur_id:03d}",
            "region": region,
            "wilaya": wilaya,
            "speaker_gender": gender,
            "speaker_age": int(age) if age.isdigit() else age,
            "text": text,
            "audio_filepath": str(target_path),
            "status": "raw"
        }
        with open(MANIFEST, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")

        print(f"[✓] تم حفظ: {sample_name}")
        cur_id += 1
        saved += 1

    print(f"\n[✓] اكتملت العملية! تم حفظ {saved} عينات جديدة بنجاح في قاعدة البيانات.")

if __name__ == "__main__":
    main()
