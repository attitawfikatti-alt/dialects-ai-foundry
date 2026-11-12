#!/usr/bin/env python3
import argparse
import torch
from transformers import WhisperForConditionalGeneration, WhisperProcessor
from peft import PeftModel

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--base_model", default="openai/whisper-small")
    p.add_argument("--lora_dir", default="whisper-dz-lora")
    p.add_argument("--out_dir", default="whisper-dz-merged")
    args = p.parse_args()

    print(f"Loading base model: {args.base_model}")
    base = WhisperForConditionalGeneration.from_pretrained(args.base_model, torch_dtype=torch.float16)
    processor = WhisperProcessor.from_pretrained(args.base_model, language="ar", task="transcribe")

    print(f"Merging LoRA weights from: {args.lora_dir}")
    model = PeftModel.from_pretrained(base, args.lora_dir)
    merged = model.merge_and_unload()

    merged.save_pretrained(args.out_dir)
    processor.save_pretrained(args.out_dir)
    print(f"Saved merged Hugging Face model to: {args.out_dir}")

if __name__ == "__main__":
    main()
