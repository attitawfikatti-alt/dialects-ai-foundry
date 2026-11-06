import json, os, shutil, subprocess, sys
from pathlib import Path
DATA_DIR, RAW_DIR = Path('data'), Path('/sdcard/Download/dialects_raw')
AUDIO_DIR, MANIFEST = DATA_DIR / 'audio', DATA_DIR / 'manifest.jsonl'
AUDIO_DIR.mkdir(parents=True, exist_ok=True); RAW_DIR.mkdir(parents=True, exist_ok=True)
def get_id():
    return (sum(1 for l in open(MANIFEST, 'r', encoding='utf-8') if l.strip()) if MANIFEST.exists() else 0) + 1
def convert(src, dst):
    return subprocess.run(['ffmpeg', '-y', '-i', str(src), '-ar', '16000', '-ac', '1', '-c:a', 'pcm_s16le', str(dst)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
def main():
    files = [f for f in RAW_DIR.iterdir() if f.suffix.lower() in ['.mp3','.m4a','.wav','.ogg','.opus','.amr']]
    if not files:
        print('[!] لا توجد تسجيلات في /sdcard/Download/dialects_raw')
        return
    cid = get_id()
    for f in files:
        print(f'
--- الملف: {f.name} ---')
        ans = input('استيراد هذا الملف؟ [Y/n]: ').strip().lower()
        if ans == 'n': continue
        reg = input('المنطقة [الغرب]: ').strip() or 'الغرب'
        wil = input('الولاية [البيض]: ').strip() or 'البيض'
        g = 'ذكر' if input('الجنس [M/F]: ').strip().upper() == 'M' else 'أنثى'
        age = input('العمر [35]: ').strip() or '35'
        txt = input('التفريغ النصي: ').strip()
        if not txt: continue
        out = AUDIO_DIR / f'sample_{cid:03d}.wav'
        if convert(f, out):
            rec = {'id': f'sample_{cid:03d}', 'region': reg, 'wilaya': wil, 'speaker_gender': g, 'speaker_age': int(age) if age.isdigit() else age, 'text': txt, 'audio_filepath': str(out), 'status': 'raw'}
            open(MANIFEST, 'a', encoding='utf-8').write(json.dumps(rec, ensure_ascii=False) + '
')
            print(f'[✓] تم حفظ: {out.name}'); cid += 1
            done = RAW_DIR / 'imported_done'; done.mkdir(exist_ok=True)
            shutil.move(str(f), str(done / f.name))
        else: print('[!] خطأ في التحويل بواسطة ffmpeg')
if __name__ == '__main__': main()
