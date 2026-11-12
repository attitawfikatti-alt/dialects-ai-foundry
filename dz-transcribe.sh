#!/data/data/com.termux/files/usr/bin/bash
set -e

if [ -z "$1" ]; then
    echo "الاستخدام: dz-transcribe <مسار_ملف_الصوت_أو_الفيديو>"
    exit 1
fi

INPUT="$1"
if [ ! -f "$INPUT" ]; then
    echo "خطأ: الملف غير موجود -> $INPUT"
    exit 1
fi

MODEL="$HOME/dialects-ai-foundry/whisper.cpp/models/ggml-whisper-dz-q5_1.bin"
CLI="$HOME/dialects-ai-foundry/whisper.cpp/whisper-cli"
TMP_WAV="${TMPDIR:-$PREFIX/tmp}/dz_input_$$.wav"
OUT_BASE="${INPUT%.*}"

ffmpeg -y -i "$INPUT" -ar 16000 -ac 1 -c:a pcm_s16le "$TMP_WAV" -loglevel error
"$CLI" -m "$MODEL" -l ar -t 4 -bs 1 -bo 1 -otxt -of "$OUT_BASE" -f "$TMP_WAV"

rm -f "$TMP_WAV"
echo "تم حفظ التفريغ النصي في: ${OUT_BASE}.txt"
