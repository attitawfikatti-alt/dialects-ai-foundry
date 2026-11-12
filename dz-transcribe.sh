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
OUT_BASE="${INPUT%.*}"

if [[ "${INPUT,,}" == *.wav ]]; then
    AUDIO_FILE="$INPUT"
    CLEANUP=0
else
    AUDIO_FILE="${TMPDIR:-$PREFIX/tmp}/dz_input_$$.wav"
    ffmpeg -y -i "$INPUT" -ar 16000 -ac 1 -c:a pcm_s16le "$AUDIO_FILE" -loglevel error
    CLEANUP=1
fi

"$CLI" -m "$MODEL" -l ar -t 4 -bs 3 -bo 3 \
    --prompt "كلام باللهجة الجزائرية:" \
    -otxt -of "$OUT_BASE" -f "$AUDIO_FILE"

if [ "$CLEANUP" -eq 1 ]; then
    rm -f "$AUDIO_FILE"
fi

echo "تم حفظ التفريغ النصي في: ${OUT_BASE}.txt"
