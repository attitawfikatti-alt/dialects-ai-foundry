import json
import subprocess
from pathlib import Path
from collections import Counter

MANIFEST = Path("dataset/manifest.jsonl")

def get_audio_duration(file_path: str) -> float:
    """حساب مدة الملف الصوتي بالثواني عبر ffprobe."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    try:
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return float(res.stdout.strip())
    except Exception:
        return 0.0

def main():
    if not MANIFEST.exists():
        print(f"[!] ملف البيانات {MANIFEST} غير موجود بعد.")
        return

    records = []
    with open(MANIFEST, "r", encoding="utf-8") as f:
        for idx, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                records.append(rec)
            except json.JSONDecodeError:
                print(f"[تحذير] خطأ في بنية السطر رقم {idx}")

    total_samples = len(records)
    if total_samples == 0:
        print("[!] لا توجد عينات مسجلة في الـ manifest.")
        return

    print("=" * 50)
    print(f"📊 تقرير فحص البيانات: {MANIFEST.name}")
    print("=" * 50)

    total_duration_sec = 0.0
    missing_files = 0
    short_texts = 0
    words_count = 0

    regions = Counter()
    wilayas = Counter()
    genders = Counter()

    for r in records:
        regions[r.get("region", "غير محدد")] += 1
        wilayas[r.get("wilaya", "غير محدد")] += 1
        genders[r.get("speaker_gender", "غير محدد")] += 1

        text = r.get("text", "").strip()
        words = text.split()
        words_count += len(words)
        if len(words) < 2:
            short_texts += 1

        audio_path = Path(r.get("audio_filepath", ""))
        if not audio_path.exists():
            missing_files += 1
        else:
            total_duration_sec += get_audio_duration(str(audio_path))

    # التحويل لساعات ودقائق
    mins, secs = divmod(total_duration_sec, 60)
    hours, mins = divmod(mins, 60)

    print(f"• إجمالي العينات (Samples):      {total_samples}")
    print(f"• إجمالي مدة الصوت:              {int(hours)}h {int(mins)}m {secs:.1f}s")
    print(f"• متوسط طول العينة:              {(total_duration_sec / total_samples):.2f} ثانية")
    print(f"• إجمالي عدد الكلمات:            {words_count} كلمة")
    print(f"• متوسط الكلمات لكل عينة:        {(words_count / total_samples):.1f} كلمة/عينة")

    print("\n--- توزيع المناطق ---")
    for reg, count in regions.most_common():
        pct = (count / total_samples) * 100
        print(f"  - {reg}: {count} عينة ({pct:.1f}%)")

    print("\n--- توزيع الولايات (أعلى 5) ---")
    for wil, count in wilayas.most_common(5):
        pct = (count / total_samples) * 100
        print(f"  - {wil}: {count} ({pct:.1f}%)")

    print("\n--- توزيع الجنس ---")
    for g, count in genders.items():
        print(f"  - {g}: {count} عينة")

    print("\n--- فحص الجودة والمشاكل ---")
    if missing_files > 0:
        print(f"  [⚠️] ملفات صوتية مفقودة: {missing_files}")
    else:
        print("  [✓] جميع ملفات الصوت موجودة وسليمة.")

    if short_texts > 0:
        print(f"  [⚠️] نصوص قصيرة جداً (أقل من كلمتين): {short_texts}")
    else:
        print("  [✓] النصوص كافية من حيث الطول.")

    print("=" * 50)

if __name__ == "__main__":
    main()
