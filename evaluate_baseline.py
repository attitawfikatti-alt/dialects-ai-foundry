import json
import os
import sys

MANIFEST_VAL = "dataset/val.jsonl"
AUDIO_DIR = "dataset/audio"

def quick_wer(ref, hyp):
    r = ref.split()
    h = hyp.split()
    d = [[0] * (len(h) + 1) for _ in range(len(r) + 1)]
    for i in range(len(r) + 1):
        d[i][0] = i
    for j in range(len(h) + 1):
        d[0][j] = j
    for i in range(1, len(r) + 1):
        for j in range(1, len(h) + 1):
            if r[i - 1] == h[j - 1]:
                d[i][j] = d[i - 1][j - 1]
            else:
                d[i][j] = 1 + min(d[i - 1][j], d[i][j - 1], d[i - 1][j - 1])
    return d[len(r)][len(h)] / max(1, len(r))

def main():
    if not os.path.exists(MANIFEST_VAL):
        print(f"[!] ملف التحقق غير موجود: {MANIFEST_VAL}")
        return

    print("=" * 55)
    print("🎙️ اختبار عينات التحقق (Validation Set Overview)")
    print("=" * 55)

    samples = []
    with open(MANIFEST_VAL, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                samples.append(json.loads(line))

    print(f"• إجمالي عينات التقييم المحجوزة: {len(samples)} عينة")
    print("• نماذج من عينات التقييم عبر الولايات:")
    
    shown = set()
    for s in samples:
        st = s.get("state", "غير محدد")
        if st not in shown:
            shown.add(st)
            print(f"  [{st}] -> المعرف: {s['id']} | النص: {s.get('normalized_text', s['text'])}")

    print("=" * 55)
    print("[✓] جاهز لتقييم النتائج ومقارنتها بنماذج ASR بعد التدريب.")

if __name__ == "__main__":
    main()
