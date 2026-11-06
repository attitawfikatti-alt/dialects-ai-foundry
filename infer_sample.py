import sys
import json
import os
import subprocess
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("الاستخدام: python infer_sample.py <sample_id_or_path>")
        print("مثال: python infer_sample.py sample_0025")
        return

    target = sys.argv[1].replace(".wav", "")
    manifest_path = Path("dataset/manifest.jsonl")
    audio_file = Path("dataset/audio") / f"{target}.wav"

    if not audio_file.exists():
        if Path(sys.argv[1]).exists():
            audio_file = Path(sys.argv[1])
        else:
            print(f"[!] لم يتم العثور على الملف الصوتي: {audio_file}")
            return

    # البحث عن البيانات المرجعية في manifest
    ground_truth = None
    metadata = {}
    if manifest_path.exists():
        with open(manifest_path, "r", encoding="utf-8") as f:
            for line in f:
                rec = json.loads(line)
                if rec.get("id") == target:
                    ground_truth = rec.get("text")
                    metadata = rec
                    break

    print("=" * 50)
    print(f"🎙️ فحص واستماع العينة: {audio_file.name}")
    print("=" * 50)
    if metadata:
        print(f"• المنطقة: {metadata.get('region', 'غير محدد')}")
        print(f"• الولاية:  {metadata.get('state', 'غير محدد')}")
        print(f"• الجنس:   {metadata.get('gender', 'غير محدد')}")
        print(f"• النص المرجعي الأصلي: \"{ground_truth}\"")
        if "normalized_text" in metadata:
            print(f"• النص الموحد:         \"{metadata['normalized_text']}\"")
    print("=" * 50)

    # تشغيل الصوت في الخلفية للمعاينة السمعية
    print("[•] جاري تشغيل المقطع الصوتي...")
    subprocess.Popen(
        ["mpv", "--no-terminal", "--really-quiet", str(audio_file)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

if __name__ == "__main__":
    main()
