#!/usr/bin/env python3
"""
dialects-ai-foundry - Audio Recording & Ingestion Tool
Records 16kHz mono WAV audio samples and updates manifest.jsonl
"""

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

DATA_DIR = Path("data")
AUDIO_DIR = DATA_DIR / "audio"
MANIFEST_FILE = DATA_DIR / "manifest.jsonl"

AUDIO_DIR.mkdir(parents=True, exist_ok=True)


def check_recording_tool():
    """التحقق من توفر أداة التسجيل باستخدام مكتبة shutil المدمجة."""
    tools = ["rec", "sox", "termux-microphone-record", "ffmpeg"]
    for tool in tools:
        if shutil.which(tool) is not None:
            return tool
    return None


def record_audio(output_path, duration=5, tool="rec"):
    """تسجيل مقطع صوتي بمعيار 16kHz Mono."""
    print(f"\n[●] يبدأ التسجيل الآن لمدة {duration} ثوانٍ... تحدث بوضوح:")
    
    if tool in ["rec", "sox"]:
        cmd = ["rec", "-r", "16000", "-c", "1", "-b", "16", str(output_path), "trim", "0", str(duration)]
        subprocess.run(cmd)
    elif tool == "termux-microphone-record":
        subprocess.run(["termux-microphone-record", "-f", str(output_path), "-l", str(duration)])
    elif tool == "ffmpeg":
        cmd = ["ffmpeg", "-y", "-f", "pulse", "-i", "default", "-ar", "16000", "-ac", "1", "-t", str(duration), str(output_path)]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    print("[✓] اكتمل التسجيل.")


def play_audio(audio_path):
    """الاستماع للمقطع المسجل للتأكد من جودته."""
    players = ["termux-media-player", "play", "mpv", "aplay"]
    for p in players:
        if shutil.which(p):
            if p == "termux-media-player":
                subprocess.Popen([p, "play", str(audio_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            elif p == "mpv":
                subprocess.run([p, "--no-video", str(audio_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                subprocess.run([p, str(audio_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return


def get_next_sample_id():
    """توليد معرف تسلسلي للعينة."""
    if not MANIFEST_FILE.exists():
        return "sample_001"
    
    count = 0
    with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                count += 1
    return f"sample_{count + 1:03d}"


def main():
    tool = check_recording_tool()
    if not tool:
        print("[!] خطأ: لم يتم العثور على أداة تسجيل مناسبة.")
        print("    قم بتثبيت الأدوات بالأمر: pkg install sox termux-api ffmpeg -y")
        sys.exit(1)

    print(f"=== dialects-ai-foundry: تسجيل عينة (الأداة: {tool}) ===")

    region = input("المنطقة [افتراضي: الغرب]: ").strip() or "الغرب"
    wilaya = input("الولاية / البلدية [افتراضي: البيض]: ").strip() or "البيض"
    gender = input("جنس المتحدث [M/F]: ").strip().upper()
    gender = "ذكر" if gender == "M" else "أنثى"
    age = input("عمر المتحدث [افتراضي: 30]: ").strip() or "30"

    while True:
        sample_id = get_next_sample_id()
        audio_filename = f"{sample_id}.wav"
        audio_path = AUDIO_DIR / audio_filename

        try:
            sec_input = input(f"\nمدة التسجيل بالثواني [افتراضي: 5]: ").strip()
            duration = int(sec_input) if sec_input else 5
        except ValueError:
            duration = 5

        input("اضغط [Enter] عندما تكون مستعداً لبدء التسجيل...")
        record_audio(audio_path, duration=duration, tool=tool)

        ans = input("\nهل تريد الاستماع للعينة للتأكد؟ [Y/n]: ").strip().lower()
        if ans in ["y", ""]:
            play_audio(audio_path)

        keep = input("هل التسجيل واضح وتريد اعتماده؟ [Y/n/r لإعادة التسجيل]: ").strip().lower()
        if keep == "r":
            if audio_path.exists():
                audio_path.unlink()
            continue
        elif keep == "n":
            if audio_path.exists():
                audio_path.unlink()
            print("[X] تم إلغاء العينة.")
            break

        text = input("\nأدخل التفريغ النصي لما قيل (باللهجة الدقيقة): ").strip()

        record = {
            "id": sample_id,
            "region": region,
            "wilaya": wilaya,
            "speaker_gender": gender,
            "speaker_age": int(age) if age.isdigit() else age,
            "text": text,
            "audio_filepath": str(audio_path),
            "status": "raw"
        }

        with open(MANIFEST_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

        print(f"\n[✓] تم حفظ العينة {sample_id} بنجاح!")

        cont = input("\nهل تريد تسجيل عينة أخرى بنفس المتحدث؟ [y/N]: ").strip().lower()
        if cont != "y":
            break

    print("\nانتهت جلسة التسجيل.")


if __name__ == "__main__":
    main()
