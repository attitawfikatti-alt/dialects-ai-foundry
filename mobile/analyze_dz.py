import warnings; warnings.filterwarnings("ignore")
import sys, os, re, glob, json, time, subprocess, tempfile, numpy as np, soundfile as sf, onnxruntime as ort

if len(sys.argv) < 2:
    print("الاستخدام:\n  1) ملف صوتي: python ~/analyze_dz.py <مسار_الملف>\n  2) ميكروفون مباشر: python ~/analyze_dz.py --mic [المدة_بالثواني]")
    sys.exit(1)

cleanup_mic = False
if sys.argv[1] == "--mic":
    dur = int(sys.argv[2]) if len(sys.argv) > 2 else 7
    audio_path = os.path.join(tempfile.gettempdir(), "mic_dz.m4a")
    if os.path.exists(audio_path):
        os.remove(audio_path)
    print(f"🎙️ جارٍ التسجيل من الميكروفون لمدة {dur} ثوانٍ... تكلّم الآن")
    subprocess.run(["termux-microphone-record", "-f", audio_path, "-l", str(dur)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(dur + 1)
    subprocess.run(["termux-microphone-record", "-q"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    cleanup_mic = True
else:
    audio_path = sys.argv[1]
    if not os.path.isfile(audio_path):
        print(f"❌ خطأ: الملف الصوتي غير موجود في المسار: {audio_path}")
        sys.exit(1)

t0 = time.time()
base_dir = os.path.expanduser("~/dialects-ai-foundry")
onnx_dir = f"{base_dir}/dialect_onnx_int8"
whisper_model = f"{base_dir}/whisper.cpp/models/ggml-whisper-dz-q5_1.bin"
whisper_bins = glob.glob(f"{base_dir}/whisper.cpp/**/whisper-cli", recursive=True) + glob.glob(f"{base_dir}/whisper.cpp/**/main", recursive=True)
whisper_bin = whisper_bins[0] if whisper_bins else "whisper-cli"
tmp_wav = os.path.join(tempfile.gettempdir(), "clean_dz.wav")

subprocess.run([
    "ffmpeg", "-y", "-i", audio_path,
    "-af", "silenceremove=start_periods=1:start_threshold=-40dB:stop_periods=-1:stop_duration=0.5:stop_threshold=-40dB",
    "-ar", "16000", "-ac", "1", tmp_wav
], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

if cleanup_mic and os.path.exists(audio_path):
    os.remove(audio_path)

if os.path.exists(f"{onnx_dir}/model_quantized.onnx"):
    audio, _ = sf.read(tmp_wav, dtype="float32")
    if len(audio) > 0:
        audio = (audio - np.mean(audio)) / (np.std(audio) + 1e-7)
        sess = ort.InferenceSession(f"{onnx_dir}/model_quantized.onnx")
        logits = sess.run(None, {"input_values": audio[None, :]})[0][0]
        probs = np.exp(logits - np.max(logits))
        probs /= np.sum(probs)
        id2label = json.load(open(f"{onnx_dir}/config.json"))["id2label"]
        top3 = np.argsort(probs)[::-1][:3]
        top_str = " | ".join([f"{id2label[str(int(i))]} ({probs[int(i)]*100:.1f}%)" for i in top3])
        print(f"📍 اللهجة / الولاية: {top_str}")

res = subprocess.run([
    whisper_bin, "-m", whisper_model, "-f", tmp_wav,
    "-l", "ar", "-t", "4",
    "--max-context", "0",
    "--entropy-thold", "2.0",
    "--no-fallback",
    "--suppress-nst", "-bs", "1", "-bo", "1", "-nt"
], capture_output=True, text=True)

raw_text = res.stdout.strip()
clean_text = re.sub(r"\b(\S+)(?:\s+\1){2,}.*$", r"\1", raw_text)
print("📝 النص المفرّغ:\n" + clean_text)
print(f"⏱️ زمن التنفيذ الإجمالي: {time.time() - t0:.1f} ثانية")
