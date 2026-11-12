# Dialects AI Foundry

Algerian Arabic ASR on Android (Termux) using whisper.cpp.

## Model
- Termuxphone/skikda-whisper-dz-ggml (q5_1, ~190MB)

## Setup
```bash
chmod +x dz-*.sh dz-review.py
for f in dz-*.sh; do ln -sf "$PWD/$f" "$PREFIX/bin/${f%.sh}"; done
ln -sf "$PWD/dz-review.py" "$PREFIX/bin/dz-review"
```

## Workflow
```bash
dz-transcribe file.m4a
dz-batch folder/
dz-split long.m4a
dz-review long_chunks/
dz-push-dataset long_chunks/ dataset-name
```
