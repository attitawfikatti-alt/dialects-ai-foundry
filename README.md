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
