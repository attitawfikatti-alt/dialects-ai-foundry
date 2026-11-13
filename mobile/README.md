# Algerian Dialect Classifier & ASR on Android (Termux CPU)

Offline pipeline running entirely on Android CPU via Termux:
- Dialect Classification (8 Wilayas): Quantized ONNX INT8 (92 MB) via onnxruntime.
- Speech-to-Text (Darja ASR): Fine-tuned Whisper quantized to GGML Q5_1 (181 MB) via whisper.cpp with silence trimming (ffmpeg) and anti-loop decoding (-bs 1 -bo 1 --max-context 0).
- Pre-quantized Weights: https://huggingface.co/Termuxphone/dialects-ai-foundry-mobile

Setup & Usage:
  python mobile/download_models.py
  python mobile/analyze_dz.py path/to/audio.aac
  python mobile/analyze_dz.py --mic
