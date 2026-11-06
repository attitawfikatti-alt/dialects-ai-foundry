import os
import json
from pathlib import Path

def create_hf_manifest(split_name, input_file, output_file):
    if not os.path.exists(input_file):
        return
    rows = []
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            rows.append({
                "audio": f"dataset/audio/{rec['id']}.wav",
                "sentence": rec.get("normalized_text", rec.get("text")),
                "original_text": rec.get("text"),
                "state": rec.get("state"),
                "region": rec.get("region"),
                "gender": rec.get("gender")
            })
    with open(output_file, "w", encoding="utf-8") as out:
        for r in rows:
            out.write(json.dumps(r, ensure_ascii=False) + "\n")
    print(f"[✓] تم تصدير قسم {split_name} لصيغة HuggingFace القياسية: {output_file} ({len(rows)} عينة)")

if __name__ == "__main__":
    create_hf_manifest("train", "dataset/train.jsonl", "dataset/train_hf.jsonl")
    create_hf_manifest("val", "dataset/val.jsonl", "dataset/val_hf.jsonl")
