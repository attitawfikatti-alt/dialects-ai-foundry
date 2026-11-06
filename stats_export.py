import os
import json
import subprocess
import pandas as pd

DATASET_CSV = "metadata/dataset.csv"
WAV_DIR = "data/wav"
JSONL_OUT = "metadata/dataset.jsonl"

def get_audio_duration(file_path):
    cmd = [
        "ffprobe", "-v", "error", "-show_entries",
        "format=duration", "-of", "default=noprint_wrappers=1:nokey=1",
        file_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True)
    try:
        return float(res.stdout.strip())
    except ValueError:
        return 0.0

def main():
    if not os.path.exists(DATASET_CSV):
        print(f"[!] ملف البيانات غير موجود: {DATASET_CSV}")
        return

    df = pd.read_csv(DATASET_CSV, dtype={"transcription": str}, encoding="utf-8-sig")
    df["transcription"] = df["transcription"].fillna("")

    total_records = len(df)
    annotated = df[df["transcription"].str.strip() != ""]
    
    total_seconds = 0.0
    jsonl_entries = []

    print("=" * 55)
    print(" dialects-ai-foundry: لوحة الإحصاء وتصدير البيانات ")
    print("=" * 55)

    for _, row in df.iterrows():
        audio_path = os.path.join(WAV_DIR, str(row["filename"]))
        dur = get_audio_duration(audio_path) if os.path.exists(audio_path) else 0.0
        total_seconds += dur

        if str(row["transcription"]).strip():
            jsonl_entries.append({
                "audio": audio_path,
                "sentence": row["transcription"],
                "speaker_id": row.get("speaker_id", "SPK01"),
                "wilaya": row.get("wilaya", "General"),
                "duration": round(dur, 2)
            })

    # حفظ نسخة JSON Lines المتوافقة مع Hugging Face
    with open(JSONL_OUT, "w", encoding="utf-8") as f:
        for entry in jsonl_entries:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    minutes = int(total_seconds // 60)
    seconds = int(total_seconds % 60)

    print(f"• إجمالي العينات الصوتية : {total_records}")
    print(f"• العينات المفرغة نصياً  : {len(annotated)}")
    print(f"• إجمالي المدة الصوتية   : {minutes} دقيقة و {seconds} ثانية")
    print(f"• نسبة التفريغ           : {(len(annotated)/total_records*100) if total_records else 0:.1f}%")
    print("=" * 55)
    print(f"[✔] تم تصدير ملف التدريب بصيغة JSONL إلى: {JSONL_OUT}")

if __name__ == "__main__":
    main()
