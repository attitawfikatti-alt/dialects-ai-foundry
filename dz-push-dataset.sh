#!/data/data/com.termux/files/usr/bin/bash
set -e

if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: dz-push-dataset <chunks_dir> <hf_dataset_name>"
    exit 1
fi

DIR="${1%/}"
REPOID="$2"

if [ ! -f "$DIR/transcripts.jsonl" ]; then
    echo "Error: transcripts.jsonl not found in $DIR"
    exit 1
fi

cp "$DIR/transcripts.jsonl" "$DIR/metadata.jsonl"
echo "Uploading dataset to Termuxphone/$REPOID..."
HF_HUB_DISABLE_XET=1 hf repo create "Termuxphone/$REPOID" --type dataset 2>/dev/null || true
HF_HUB_DISABLE_XET=1 hf upload "Termuxphone/$REPOID" "$DIR" . --repo-type dataset --exclude "*.txt" --exclude "transcripts.jsonl"
echo "Done! Dataset live at: https://huggingface.co/datasets/Termuxphone/$REPOID"
