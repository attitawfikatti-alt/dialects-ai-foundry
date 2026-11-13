import os, hashlib
from huggingface_hub import hf_hub_download

repo_id = "Termuxphone/dialects-ai-foundry-mobile"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
onnx_dir = os.path.join(base_dir, "dialect_onnx_int8")
whisper_dir = os.path.join(base_dir, "whisper.cpp", "models")
HASHES = {"dialect_onnx_int8/model_quantized.onnx": "fd82b8f9b987fc1cdd188c267077b7e0f98ae4e9c16529a5cf36204ee19c27c4", "dialect_onnx_int8/config.json": "8f7618bc4f4a61e424d8cd3a16ef3b31dd7ad750a660a0f2d05dbf739756a20c", "ggml-whisper-dz-q5_1.bin": "aa1251e571b4c4b01797adee9bf118f5e9421e2a60aedf8df2d0a0687a983c06"}

def check(p, exp):
    if hashlib.sha256(open(p, "rb").read()).hexdigest() != exp:
        os.remove(p); raise RuntimeError(f"SHA256 mismatch: {p}")

os.makedirs(onnx_dir, exist_ok=True); os.makedirs(whisper_dir, exist_ok=True)
for f in ["model_quantized.onnx", "config.json"]:
    rel = f"dialect_onnx_int8/{f}"
    check(hf_hub_download(repo_id=repo_id, filename=rel, local_dir=base_dir), HASHES[rel])
check(hf_hub_download(repo_id=repo_id, filename="ggml-whisper-dz-q5_1.bin", local_dir=whisper_dir), HASHES["ggml-whisper-dz-q5_1.bin"])
print("✅ Models downloaded and SHA256 verified!")
