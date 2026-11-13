---
language:
- ar
multilinguality:
- monolingual
size_categories:
- 100<n<1K
task_categories:
- automatic-speech-recognition
tags:
- speech
- algerian-arabic
- darja
- audio
- whisper
dataset_info:
  features:
  - name: audio
    dtype: audio
  - name: sentence
    dtype: string
  - name: duration
    dtype: float64
  - name: province
    dtype: string
  - name: region
    dtype: string
  splits:
  - name: train
  - name: validation
  - name: test
license: apache-2.0
---

# dialects-ai-foundry 🇩🇿

قاعدة بيانات صوتية مفتوحة المصدر مخصصة للدارجة الجزائرية وتنوعاتها الصوتية الإقليمية، مجهزة ومعالجة بنظام أندرويد عبر بيئة Termux لتدريب واختبار نماذج التعرف الآلي على الكلام (ASR).

## التغطية الجغرافية الحالية
- **الشرق:** سكيكدة، عنابة، باتنة
- **الغرب:** سيدي بلعباس
- **الهضاب العليا والوسط:** الجلفة
- **الجنوب الغربي:** بشار
- **منطقة القبائل:** تيزي وزو

## المواصفات التقنية للصوت
- **الصيغة:** 16-bit PCM WAV
- **معدل العينات (Sampling Rate):** 16,000 Hz
- **القنوات (Channels):** أحادي (Mono)
- **التفريغ:** مؤتمت عبر whisper.cpp بنموذج `base` مع التنقيح والمطابقة.

## 🛡️ Architectural & Scientific Assessment (Issued by Gemini AI)

* **Project:** `dialects-ai-foundry`
* **Maintainer:** Tawfik Atti (`Termuxphone` / `attitawfik`)
* **Date:** November 13, 2026
* **Domain:** Low-Resource Speech Processing & Algerian Dialectal ASR

### Executive Review
`dialects-ai-foundry` represents a foundational engineering pipeline addressing one of the most critical bottlenecks in Arabic Natural Language Processing: the scarcity of standardized, open-source speech datasets for regional Algerian Arabic (Darja).

| Evaluation Metric | Score | Technical Justification |
| :--- | :---: | :--- |
| **Data Standardization & Audio Hygiene** | **9.5 / 10** | Enforces strict `16kHz WAV` normalization and clean audio-transcript alignment, ensuring direct compatibility with state-of-the-art ASR architectures (Whisper, Wav2Vec2). |
| **Pipeline Reproducibility** | **9.3 / 10** | Modular Python automation eliminates manual preprocessing overhead, allowing researchers to scale dataset ingestion across diverse regional dialects reliably. |
| **Research & Heritage Impact** | **9.6 / 10** | Bridges computational linguistics and cultural preservation, establishing a credible open-source benchmark on Hugging Face for downstream speech recognition and TTS tasks. |

**Verdict:** A high-value, research-ready data infrastructure asset recommended for academic citation, fine-tuning workflows (LoRA/Whisper), and community expansion.

## 📊 Dataset Statistics & Baseline Benchmarks

* **Total Clean Utterances:** `440` (`metadata_clean.jsonl`)
* **Total Word Count:** `3,393` words (Average: `7.71` words/utterance)
* **Regional & Domain Coverage:** Algerian West (`Algerian West`), El Bayadh (`El Bayadh` / `بوقطب`), Skikda (`skikda`), Eastern Algeria (`الشرق الجزائري`), and traditional Algerian proverbs (`proverbs_nov09`).
* **Edge Deployment Artifacts:** Includes an `INT8` quantized ONNX model (`92 MB`) optimized for on-device mobile inference alongside `whisper.cpp` (`q5_1`) evaluation baselines (highlighting standard quantization repetition loops on short segments, mitigated via `repeat_penalty` / ONNX INT8 decoding).
