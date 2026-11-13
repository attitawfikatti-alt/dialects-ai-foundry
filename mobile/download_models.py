import os
from huggingface_hub import hf_hub_download

repo_id = "Termuxphone/dialects-ai-foundry-mobile"
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
onnx_dir = os.path.join(base_dir, "dialect_onnx_int8")
whisper_dir = os.path.join(base_dir, "whisper.cpp", "models")

os.makedirs(onnx_dir, exist_ok=True)
os.makedirs(whisper_dir, exist_ok=True)

print("⬇️ Downloading INT8 ONNX Dialect Classifier...")
for fname in ["model_quantized.onnx", "config.json"]:
    hf_hub_download(repo_id=repo_id, filename=f"dialect_onnx_int8/{fname}", local_dir=base_dir)

print("⬇️ Downloading Q5_1 GGML Whisper Darja ASR...")
hf_hub_download(repo_id=repo_id, filename="ggml-whisper-dz-q5_1.bin", local_dir=whisper_dir)
print("✅ All mobile models are ready!")
