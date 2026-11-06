import subprocess
import re
from pathlib import Path

RAW_DIR = Path("raw_audio")
TEMP_DIR = Path("temp_segments")
TEMP_DIR.mkdir(parents=True, exist_ok=True)

def get_silence_intervals(audio_path, noise_db="-25dB", silence_dur=0.25):
    cmd = [
        "ffmpeg", "-i", str(audio_path),
        "-af", f"silencedetect=noise={noise_db}:d={silence_dur}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, errors="replace")
    
    starts = [float(x) for x in re.findall(r"silence_start:\s*([\d\.]+)", res.stderr)]
    ends = [float(x) for x in re.findall(r"silence_end:\s*([\d\.]+)", res.stderr)]
    
    dur_match = re.search(r"Duration:\s*(\d+):(\d+):([\d\.]+)", res.stderr)
    total_dur = 0.0
    if dur_match:
        h, m, s = dur_match.groups()
        total_dur = int(h) * 3600 + int(m) * 60 + float(s)
        
    intervals = []
    prev_end = 0.0
    for s_start, s_end in zip(starts, ends):
        if s_start > prev_end:
            intervals.append((prev_end, s_start))
        prev_end = s_end
        
    if total_dur > prev_end:
        intervals.append((prev_end, total_dur))
        
    return intervals

def split_all():
    raw_files = [f for f in RAW_DIR.glob("*.*") if f.suffix.lower() in {".mp3", ".wav", ".m4a", ".aac", ".ogg"}]
    if not raw_files:
        print("[!] لا توجد ملفات في raw_audio/")
        return

    for old in TEMP_DIR.glob("*.wav"):
        old.unlink()

    total_extracted = 0
    for rf in raw_files:
        print(f"\n[•] جاري فحص: {rf.name}")
        intervals = get_silence_intervals(rf)
        
        extracted = 0
        for i, (start, end) in enumerate(intervals):
            dur = end - start
            if 1.2 <= dur <= 14.0:
                out_path = TEMP_DIR / f"{rf.stem}_seg_{i:04d}.wav"
                cmd = [
                    "ffmpeg", "-y",
                    "-ss", f"{start:.3f}",
                    "-to", f"{end:.3f}",
                    "-i", str(rf),
                    "-ar", "16000",
                    "-ac", "1",
                    "-vn",
                    str(out_path)
                ]
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                extracted += 1
                total_extracted += 1

        print(f"[✓] تم استخراج {extracted} مقطع صالح.")

    print(f"\n[✓] إجمالي المقاطع الجاهزة في temp_segments: {total_extracted}")

if __name__ == "__main__":
    split_all()
