import os
import shutil
import subprocess
import pandas as pd
from datetime import datetime

DATASET_CSV = "metadata/dataset.csv"
PROCESSED_DIR = "data/wav"
INBOX_DIR = "data/inbox"

os.makedirs(PROCESSED_DIR, exist_ok=True)
os.makedirs(INBOX_DIR, exist_ok=True)
os.makedirs("metadata", exist_ok=True)

if not os.path.exists(DATASET_CSV):
    df_init = pd.DataFrame(columns=[
        "audio_id", "filename", "speaker_id", "region", "wilaya", 
        "transcription", "context_type", "timestamp"
    ])
    df_init.to_csv(DATASET_CSV, index=False, encoding="utf-8-sig")

def get_audio_files(directory):
    valid_exts = ('.mp3', '.m4a', '.wav', '.ogg', '.aac', '.opus')
    return [f for f in os.listdir(directory) if f.lower().endswith(valid_exts)]

def process_file(file_path, speaker_id, region, wilaya, context_type):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = f"{wilaya}_{speaker_id}_{timestamp}"
    processed_path = os.path.join(PROCESSED_DIR, f"{base_name}.wav")

    print(f"\n[+] جاري تحويل {os.path.basename(file_path)} إلى 16kHz Mono WAV...")
    res = subprocess.run([
        "ffmpeg", "-y", "-i", file_path,
        "-ar", "16000", "-ac", "1",
        processed_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if res.returncode != 0:
        print(f"[!] خطأ في معالجة الملف {file_path}")
        return False

    print(f"[✔] تم التحويل: {processed_path}")
    transcription = input("[?] التفريغ النصي للمقطع (أو اضغط Enter لتجاوزه): ").strip()

    row = {
        "audio_id": base_name,
        "filename": f"{base_name}.wav",
        "speaker_id": speaker_id,
        "region": region,
        "wilaya": wilaya,
        "transcription": transcription,
        "context_type": context_type,
        "timestamp": timestamp
    }
    df = pd.DataFrame([row])
    df.to_csv(DATASET_CSV, mode="a", header=False, index=False, encoding="utf-8-sig")
    return True

def main():
    print("=" * 55)
    print(" dialects-ai-foundry: محطة استيراد وتوثيق اللهجات ")
    print("=" * 55)
    
    # خياران: مجلد inbox الداخلي أو مجلد التسجيلات بالهاتف
    phone_records = os.path.expanduser("~/storage/shared/Recordings")
    if not os.path.exists(phone_records):
        phone_records = os.path.expanduser("~/storage/downloads")

    print("خيارات مسار الصوتيات:")
    print(f"1) فحص مجلد الهاتف: {phone_records}")
    print(f"2) فحص مجلد المشروع الداخلي: {INBOX_DIR}")
    
    choice = input("اختر المسار [1 أو 2، الافتراضي 1]: ").strip()
    target_dir = phone_records if choice != "2" else INBOX_DIR

    files = get_audio_files(target_dir)
    if not files:
        print(f"\n[!] لا توجد ملفات صوتية مدعومة داخل: {target_dir}")
        print(f"ضع تسجيلاتك هناك أو داخل {INBOX_DIR} ثم أعد التشغيل.")
        return

    print(f"\n[+] تم العثور على {len(files)} تسجيل.")
    speaker_id = input("معرّف المتحدث [SPK01]: ").strip() or "SPK01"
    wilaya = input("الولاية [ElBayadh]: ").strip() or "ElBayadh"
    region = input("المنطقة / العرش [N/A]: ").strip() or "N/A"
    context_type = input("نوع المحتوى (حوار / ملحون / أمثال): ").strip() or "dialogue"

    for f in files:
        full_path = os.path.join(target_dir, f)
        print(f"\n--- معالجة: {f} ---")
        act = input("معالجة هذا الملف؟ [Y/n/q للخروج]: ").strip().lower()
        if act == 'q':
            break
        if act == 'n':
            continue
        process_file(full_path, speaker_id, region, wilaya, context_type)

    print("\n[✔] اكتملت الجلسة. تم تحديث metadata/dataset.csv بنجاح.")

if __name__ == "__main__":
    main()
