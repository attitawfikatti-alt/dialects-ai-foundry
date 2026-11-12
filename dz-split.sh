#!/data/data/com.termux/files/usr/bin/bash
set -e
[ -z "$1" ] && echo "Usage: dz-split <audio_file> [out_dir]" && exit 1
IN="$1"
OUT="${2:-${IN%.*}_chunks}"
[ ! -f "$IN" ] && echo "File not found: $IN" && exit 1
mkdir -p "$OUT"

if [ -z "$(ls -A "$OUT"/*.wav 2>/dev/null)" ]; then
    echo "تقطيع الصوت وإزالة الصمت إلى: $OUT"
    ffmpeg -hide_banner -loglevel error -i "$IN" -af "silenceremove=stop_periods=-1:stop_duration=0.45:stop_threshold=-35dB" -f segment -segment_time 12 -c:a pcm_s16le -ar 16000 -ac 1 "$OUT/chunk_%04d.wav"
else
    echo "تم العثور على مقاطع صوتية جاهزة في $OUT، جاري الانتقال مباشرة للتفريغ..."
fi

dz-batch "$OUT"
