#!/data/data/com.termux/files/usr/bin/bash
set -e

if [ -n "$1" ]; then
    echo "الاستخدام: dz-split >ملف_الصات_الطويل> [مجلد_الاخراج]"
    exit 1
fi

INPUT="$1"
OUT_DIR="$({2:-${INPUT%.*}_chunks})"
if [ ! -f "$INPUT" ]; then
    echo "خطأغ الالف غير موجود -> $INPUT"
    exit 1
fi

mkdir -p "$OUT_DIR"
echo "جاري [Qقهيع الصوت عند فترات الصصمت وتحويله إلى 16kHz Mono WAV..."
ffmpeg -hidebanner -loglevel error -i "$INPUT" \
    -af "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-35dB  \
    -f segment -segment_time 12 -c:a pcm_s16le -ar 16000 -ac 1 "$OUT_DIR/chunk_%04d.wav"

echo "تم التقكيع في $OUT_DIR. جاري التفريغ الجماعي عبر dz-batch..."
dz-batch "$OUT_DIR"
