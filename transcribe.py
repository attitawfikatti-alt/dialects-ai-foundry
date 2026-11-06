import sys
import json
import shutil
import subprocess
from pathlib import Path

AUDIO_DIR = Path("dataset/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MANIFEST = Path("dataset/manifest.jsonl")

def safe_input(prompt: str) -> str:
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\n\n[!] تم إيقاف السكربت يدوياً.")
        sys.exit(0)

class AudioPlayer:
    """مشغل صوت يعمل في الخلفية بالتوازي دون حظر الإدخال."""
    def __init__(self):
        self.proc = None

    def play(self, file_path: Path, loop: bool = False):
        self.stop()
        cmd = ["mpv", "--no-video", "--really-quiet"]
        if loop:
            cmd.append("--loop=inf")
        cmd.append(str(file_path))
        
        try:
            # تشغيل في الخلفية دون انتظار Popen
            self.proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("[تحذير] برنامج mpv غير مثبت. شغّل: pkg install mpv")

    def stop(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            try:
                self.proc.wait(timeout=0.2)
            except Exception:
                self.proc.kill()
            self.proc = None

player = AudioPlayer()

def get_next_sample_id():
    if not MANIFEST.exists():
        return 1
    count = 0
    with open(MANIFEST, "r", encoding="utf-8") as f:
        for _ in f:
            count += 1
    return count + 1

def process_segments(segments, reg, wil, g, age):
    cid = get_next_sample_id()
    saved = 0

    print(f"\n[i] سيتم بدء الترقيم من العينة رقم: sample_{cid:04d}")

    for s in segments:
        print(f"\n--------------------------------------------------")
        print(f"[▶] جاري تشغيل المقطع في الخلفية: {s.name}")
        
        # تشغيل المقطع في الخلفية (مرة واحدة أو يتكرر حسب رغبتك)
        # إذا أردته يتكرر باستمرار أثناء الكتابة، اجعلها: player.play(s, loop=True)
        player.play(s, loop=True)

        while True:
            prompt_text = "✍️ اكتب التفريغ (أو اكتب: r=إعادة / s=تخطي / q=خروج): "
            txt = safe_input(prompt_text)

            # أوامر التحكم السريع
            if txt.lower() == "r":
                player.play(s, loop=True)
                continue
            elif txt.lower() == "s":
                player.stop()
                print(f"[x] تم تخطي وحذف المقطع: {s.name}")
                s.unlink(missing_ok=True)
                break
            elif txt.lower() == "q":
                player.stop()
                print(f"\n[✓] انتهت الجلسة! تم حفظ {saved} عينة.")
                return
            elif txt == "":
                # إذا ضغط Enter بدون كتابة شيء
                continue
            else:
                # بمجرد كتابة النص والضغط على Enter، نوقف الصوت فوراً
                player.stop()

                sample_name = f"sample_{cid:04d}.wav"
                dst = AUDIO_DIR / sample_name
                shutil.move(str(s), str(dst))

                rec = {
                    "id": f"sample_{cid:04d}",
                    "region": reg,
                    "wilaya": wil,
                    "speaker_gender": g,
                    "speaker_age": int(age) if age.isdigit() else age,
                    "text": txt,
                    "audio_filepath": str(dst),
                    "status": "verified"
                }

                with open(MANIFEST, "a", encoding="utf-8") as f:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")

                print(f"[✓] تم حفظ: {sample_name}")
                cid += 1
                saved += 1
                break

    player.stop()
    print(f"\n[✓] انتهت جميع المقاطع! تم حفظ {saved} عينة جديدة.")

def main():
    print("=" * 45)
    print("  أداة تفريغ العينات الصوتية (تشغيل بالخلفية)  ")
    print("=" * 45)

    temp_dir = Path("temp_segments")
    if not temp_dir.exists():
        print(f"[!] المجلد {temp_dir} غير موجود.")
        return

    segments = sorted(list(temp_dir.glob("*.wav")))
    if not segments:
        print("[!] لم يتم العثور على مقاطع جاهزة في temp_segments/.")
        return

    print(f"[i] تم العثور على {len(segments)} مقطع بانتظار التفريغ.")
    
    reg = safe_input("المنطقة (الوسط / الشرق / الغرب / الجنوب): ")
    wil = safe_input("الولاية (مثال: 16 - الجزائر / 31 - وهران): ")
    g = safe_input("الجنس (M/F): ").upper()
    age = safe_input("العمر: ")

    process_segments(segments, reg, wil, g, age)

if __name__ == "__main__":
    main()
