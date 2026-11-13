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


---

## 💼 Commercial Licensing & Enterprise Solutions (الترخيص التجاري وحلول الشركات)

While the open-source codebase and pre-quantized weights (`Termuxphone/dialects-ai-foundry-mobile`) are released under **CC BY-NC 4.0** for non-commercial research and educational use, **commercial licenses** and custom deployments are available for businesses, call centers, telecom operators, and fintech/enterprise applications.

**Available Enterprise Services:**
- **On-Premise / Air-Gapped Deployment:** Full offline Algerian Darja ASR & Wilaya dialect routing deployed on your local servers (100% compliant with data privacy laws such as Algerian Law 18-07).
- **Custom Domain Fine-Tuning:** Tailoring speech recognition and dialect models to your industry vocabulary (banking, customer support, logistics, medical).
- **Mobile & Edge SDK Integration:** Lightweight INT8 ONNX & GGML Q5_1 models embedded directly into Android/iOS apps with zero cloud latency.

📩 **For commercial licensing, custom datasets, or consulting inquiries:**  
**Email:** `attitawfikatti@gmail.com`  
**GitHub:** [@attitawfikatti-alt](https://github.com/attitawfikatti-alt) | **Hugging Face:** [@Termuxphone](https://huggingface.co/Termuxphone)

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
