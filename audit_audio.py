import os
import wave
import glob

files = glob.glob("**/*.wav", recursive=True)
if not files:
    print("لم يتم العثور على أي ملفات .wav في المسار الحالي.")
    exit()

total_duration = 0.0
sample_rates = set()
channels = set()
valid_files = 0
corrupted_files = []

for f in files:
    try:
        with wave.open(f, 'rb') as w:
            n_frames = w.getnframes()
            rate = w.getframerate()
            chan = w.getnchannels()
            duration = n_frames / float(rate)
            total_duration += duration
            sample_rates.add(rate)
            channels.add(chan)
            valid_files += 1
    except Exception as e:
        corrupted_files.append((f, str(e)))

print("=== تقرير فحص المقاطع الصوتية ===")
print(f"الملفات المفحوصة بنجاح: {valid_files} / {len(files)}")
print(f"إجمالي المدة الصوتية: {total_duration / 60:.2f} دقيقة ({total_duration:.1f} ثانية)")
print(f"معدلات التردد (Sample Rates): {sorted(list(sample_rates))} Hz")
print(f"القنوات (Channels): {list(channels)} (1=Mono, 2=Stereo)")

if corrupted_files:
    print(f"\nتنبيه: يوجد {len(corrupted_files)} ملف غير صالح أو تالف:")
    for f, err in corrupted_files[:5]:
        print(f"- {f}: {err}")
else:
    print("\nجميع ملفات الصوت سليمة ومطابقة لمعايير WAV.")
