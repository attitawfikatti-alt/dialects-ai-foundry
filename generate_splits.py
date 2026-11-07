import os, glob, json, random

random.seed(42)  # لضمان ثبات التقسيم عند إعادة التشغيل

data_dir = "data"
all_records = []

# جمع السجلات من كل المانيفستات الموجودة
manifest_files = glob.glob(f"{data_dir}/**/manifest.jsonl", recursive=True)

for mf in manifest_files:
    region_dir = os.path.dirname(mf)
    with open(mf, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                # التأكد من صحة مسار الصوت النسبي بالنسبة للمشروع ككل
                audio_file = row.get("audio_file") or row.get("audio_filepath", "")
                if not audio_file.startswith("data/"):
                    full_audio = os.path.normpath(os.path.join(region_dir, audio_file))
                else:
                    full_audio = audio_file

                transcript = row.get("transcript") or row.get("text", "")
                transcript = " ".join(transcript.strip().split())  # تنظيف المسافات والأسطر

                # نقبل فقط العينات التي تحوي صوتاً موجوداً ونصاً غير فارغ
                if transcript and os.path.exists(full_audio):
                    all_records.append({
                        "audio": full_audio,
                        "duration": float(row.get("duration", 0.0)),
                        "sentence": transcript,
                        "province": row.get("province", os.path.basename(region_dir)),
                        "region": row.get("region", "الجزائر")
                    })
            except Exception:
                continue

print(f"[*] إجمالي العينات الصالحة والمفرغة: {len(all_records)}")

# خلط العينات
random.shuffle(all_records)

# حساب نسب التقسيم
n_total = len(all_records)
n_val = max(1, int(n_total * 0.10))
n_test = max(1, int(n_total * 0.10))
n_train = n_total - n_val - n_test

train_set = all_records[:n_train]
val_set = all_records[n_train:n_train + n_val]
test_set = all_records[n_train + n_val:]

splits = {
    "train.jsonl": train_set,
    "validation.jsonl": val_set,
    "test.jsonl": test_set
}

os.makedirs("splits", exist_ok=True)
for filename, dataset in splits.items():
    out_path = os.path.join("splits", filename)
    with open(out_path, "w", encoding="utf-8") as f:
        for item in dataset:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    print(f"[+] تم إنشاء {out_path} بحجم {len(dataset)} عينة")

