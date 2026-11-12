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

# 3. Install the transcription wrappers
chmod +x dz-transcribe.sh dz-batch.sh
ln -sf "$PWD/dz-transcribe.sh" "$PREFIX/bin/dz-transcribe"
ln -sf "$PWD/dz-batch.sh" "$PREFIX/bin/dz-batch"
```

## Usage

Ranscribe a single audio or video file:
```bash
dz-transcribe path/to/audio.m4a
```

Batch-transcribe an entire folder and generate `¶¶§±Êâ¦Û#²‰å`:
```bash
dz-batch path/to/audio_folder
```
