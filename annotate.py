import os
import subprocess
import pandas as pd

DATASET_CSV = "metadata/dataset.csv"
WAV_DIR = "data/wav"

def play_audio(file_path):
    res = subprocess.run(["termux-media-player", "play", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode != 0:
        subprocess.run(["termux-open", "--view", file_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    if not os.path.exists(DATASET_CSV):
        print(f"[!] ملف البيانات غير موجود: {DATASET_CSV}")
        return

    df = pd.read_csv(DATASET_CSV, dtype={"transcription": str}, encoding="utf-8-sig")
    df["transcription"] = df["transcription"].fillna("")

    total_samples = len(df)
    missing_indices = df[df["transcription"].str.strip() == ""].index

    print("=" * 55)
    print(" dialects-ai-foundry: محطة المراجعة والتفريغ النصي ")
    print("=" * 55)
    print(f"[i] إجمالي العينات المسجلة: {total_samples}")
    print(f"[i] العينات بانتظار التفريغ: {len(missing_indices)}")
    print("=" * 55)

    if len(missing_indices) == 0:
        print("[✔] جميع التسجيلات الحالية مفرغة نصياً بنجاح!")
        return

    for idx in missing_indices:
        row = df.loc[idx]
        audio_file = os.path.join(WAV_DIR, str(row["filename"]))
        print(f"\n--- العينة: {row['filename']} ---")
        print(f"الولاية: {row['wilaya']} | المتحدث: {row['speaker_id']} | النوع: {row['context_type']}")

        if not os.path.exists(audio_file):
            print(f"[!] تحذير: الملف الصوتي غير موجود في {audio_file}")
            continue

        while True:
            action = input("\n[p] سماع المقطع | [t] إدخال التفريغ | [s] تجاوز | [q] خروج: ").strip().lower()

            if action == 'p':
                print("[▶] جاري التشغيل...")
                play_audio(audio_file)
            elif action == 't':
                text = input("[?] اكتب النص بدقة: ").strip()
                if text:
                    df.at[idx, "transcription"] = text
                    df.to_csv(DATASET_CSV, index=False, encoding="utf-8-sig")
                    print("[✔] تم حفظ التفريغ.")
                    break
            elif action == 's':
                print("تم التجاوز.")
                break
            elif action == 'q':
                print("إغلاق أداة التفريغ.")
                return

if __name__ == "__main__":
    main()
