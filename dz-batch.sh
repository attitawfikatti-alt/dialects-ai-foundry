#!/data/data/com.termux/files/usr/bin/bash
set -e

if [ -z "$1" ]; then
    echo "الاستخدام: dz-batch <مسار_المجلد>"
    exit 1
fi

DIR="${1%/}"
if [ ! -d "$DIR" ]; then
    echo "خطأ: المجلد غير موجود -> $DIR"
    exit 1
fi

OUT_JSONL="$DIR/transcripts.jsonl"
touch "$OUT_JSONL"

shopt -s nullglob nocaseglob
FILES=("$DIR"/*.{wav,mp3,ogg,m4a,opus,mp4,aac,flac})

if [ ${#FILES[@]} -eq 0 ]; then
    echo "لم يتم العثور على ملفات صوتية أو فيديو مدعومة في: $DIR"
    exit 1
fi

echo "جاري فحص وتفريغ ${#FILES[@]} ملف (مع تخطي المنجز مسبقاً)..."
for FILE in "${FILES[@]}"; do
    BASENAME=$(basename "$FILE")
    if grep -q "\"$BASENAME\"" "$OUT_JSONL"; then
        continue
    fi
    echo "----------------------------------------"
    echo "معالجة: $BASENAME"
    dz-transcribe "$FILE"
    TXT_FILE="${FILE%.*}.txt"
    if [ -f "$TXT_FILE" ]; then
        TEXT=$(tr '\n' ' ' < "$TXT_FILE" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')
        python3 -c 'import json, sys; print(json.dumps({"file_name": sys.argv[1], "text": sys.argv[2]}, ensure_ascii=False))' "$BASENAME" "$TEXT" >> "$OUT_JSONL"
    fi
done

echo "========================================"
echo "اكتمل التفريغ الجماعي! الإجمالي في $OUT_JSONL: $(wc -l < "$OUT_JSONL") سطر."
