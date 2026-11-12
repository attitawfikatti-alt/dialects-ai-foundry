# Dialects AI Foundry (Algerian Arabic ASR)

Open-source Algerian Arabic multi-dialect speech recognition pipeline built on **whisper.cpp** and optimized for offline inference on Android (Termux).

## Pre-trained GGML Model

The quantized `q5_1` model (~190 MB) is hosted on Hugging Face:
- [**Termuxphone/skikda-whisper-dz-ggml**](https://huggingface.co/Termuxphone/skikkda-whisper-dz-ggml)

## Quick Installation (Termux)

```bash
# 1. Clone the repository
git clone https://github.com/attitawfikatti-alt/dialects-ai-foundry.git
cd dialects-ai-foundry

# 2. Download the quantized model
mkdir -p whisper.cpp/models
repo="https://huggingface.co/Termuxphone/skikkda-whisper-dz-ggml/resolve/main"
curl -L "$repo/ggml-whisper-dz-q5_1.bin" -o whisper.cpp/models/ggml-whisper-dz-q5_1.bin

# 3. Install the CLI wrappers
chmod +x dz-transcribe.sh dz-batch.sh dz-split.sh dz-push-dataset.sh
for script in dz-transcribe dz-batch dz-split dz-push-dataset; do
  ln -sf "$PWD/${script}.sh" "$PREFIX/bin/${script}"
done
```

## CLI Workflow

```bash
# 1. Transcribe a single audio/video file
dz-transcribe audio.m4a

# 2. Batch-transcribe a folder into transcripts.jsonl
dz-batch audio_folder

# 3. Auto-split long audio by silence and batch-transcribe
dzi-split long_recording.m4a

# 4. Push chunks + metadata.jsonl to Hugging Face Datasets
dz-push-dataset long_recording_chunks dz-dialect-dataset
```
