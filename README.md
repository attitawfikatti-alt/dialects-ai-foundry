---
language:
- ar
- arq
license: cc-by-nc-4.0
task_categories:
- automatic-speech-recognition
pretty_name: Algerian Multi-Dialect Speech Corpus (dialects-ai-foundry)
size_categories:
- n<1K
tags:
- algerian-arabic
- darja
- whisper
- asr
- speech
---

# Algerian Multi-Dialect Speech Corpus (dialects-ai-foundry)

An open-source speech recognition (ASR) dataset covering diverse Algerian regional dialects (Skikda, Sidi Bel Abbes, Annaba, Djelfa, Batna, Tizi Ouzou, Tebessa, Bechar, and Ouargla).

## Dataset Structure
- splits/train_ready.jsonl: 218 unique deduplicated training samples.
- splits/validation_ready.jsonl: 27 unique validation samples.
- splits/test_ready.jsonl: 27 unique test samples.
- data/<wilaya>/wavs/: 16kHz mono .wav audio segments mapped via relative paths.
