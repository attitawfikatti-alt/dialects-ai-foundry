import json
from collections import defaultdict
import torch
import evaluate
from datasets import load_dataset, Audio
from transformers import pipeline

DATASET_ID = "Termuxphone/dialects-ai-foundry"
FINE_TUNED_ID = "Termuxphone/whisper-small-algerian-merged"
BASE_ID = "openai/whisper-small"

device = 0 if torch.cuda.is_available() else -1
wer_metric = evaluate.load("wer")

print("Loading held-out test split (27 verified samples)...")
ds = load_dataset(DATASET_ID, split="test")
ds = ds.cast_column("audio", Audio(sampling_rate=16000))

print(f"Loading fine-tuned model: {FINE_TUNED_ID}...")
ft_pipe = pipeline("automatic-speech-recognition", model=FINE_TUNED_ID, device=device)

print(f"Loading baseline model: {BASE_ID}...")
base_pipe = pipeline("automatic-speech-recognition", model=BASE_ID, device=device)

gen_kwargs = {"language": "arabic", "task": "transcribe"}
results_by_province = defaultdict(lambda: {"refs": [], "ft_preds": [], "base_preds": []})

for row in ds:
    prov = row.get("province", "unknown")
    audio_input = row["audio"]
    ref_text = row["text"].strip()

    ft_pred = ft_pipe(audio_input, generate_kwargs=gen_kwargs)["text"].strip()
    base_pred = base_pipe(audio_input, generate_kwargs=gen_kwargs)["text"].strip()

    results_by_province[prov]["refs"].append(ref_text)
    results_by_province[prov]["ft_preds"].append(ft_pred)
    results_by_province[prov]["base_preds"].append(base_pred)

print("\n### Per-Dialect WER Benchmark (Test Set)\n")
print("| Province / Dialect | Samples | Whisper-Small (Base) WER | dialects-ai-foundry WER | Improvement |")
print("| :--- | :---: | :---: | :---: | :---: |")

all_refs, all_ft, all_base = [], [], []

for prov in sorted(results_by_province.keys()):
    data = results_by_province[prov]
    n = len(data["refs"])
    base_wer = wer_metric.compute(predictions=data["base_preds"], references=data["refs"]) * 100
    ft_wer = wer_metric.compute(predictions=data["ft_preds"], references=data["refs"]) * 100
    diff = base_wer - ft_wer
    sign = "+" if diff > 0 else ""
    print(f"| `{prov}` | {n} | {base_wer:.2f}% | **{ft_wer:.2f}%** | {sign}{diff:.2f}% |")

    all_refs.extend(data["refs"])
    all_ft.extend(data["ft_preds"])
    all_base.extend(data["base_preds"])

total_base = wer_metric.compute(predictions=all_base, references=all_refs) * 100
total_ft = wer_metric.compute(predictions=all_ft, references=all_refs) * 100
total_diff = total_base - total_ft
print(f"| **OVERALL (All Dialects)** | **{len(all_refs)}** | **{total_base:.2f}%** | **{total_ft:.2f}%** | **+{total_diff:.2f}%** |")
