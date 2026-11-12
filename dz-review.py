#!/usr/bin/env python3
import json, os, sys, subprocess, shutil

target = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "."
path = os.path.join(target, "transcripts.jsonl") if os.path.isdir(target) else target
if not os.path.exists(path):
    sys.exit(f"Error: {path} not found")

base_dir = os.path.dirname(os.path.abspath(path))
prog_path = path + ".progress"
player = next((shutil.which(p) for p in ("mpv", "termux-media-player", "play") if shutil.which(p)), None)

with open(path, "r", encoding="utf-8") as f:
    items = [json.loads(line) for line in f if line.strip()]

done = {}
if os.path.exists(prog_path):
    with open(prog_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                r = json.loads(line)
                done[r["file_name"]] = r

print(f"\n=== DZ Reviewer | {len(done)}/{len(items)} done ===")
print("Enter=accept | text=edit | r=replay | d=delete | q=quit\n")
for idx, item in enumerate(items, 1):
    fname = item["file_name"]
    if fname in done:
        continue
    audio = os.path.join(base_dir, fname)
    text = item["text"]
    while True:
        print(f"[{idx}/{len(items)}] {fname}\nText: {text}")
        if player:
            subprocess.run([player, audio], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        cmd = input("> ").strip()
        if cmd == "r":
            continue
        if cmd == "q":
            sys.exit("Progress saved.")
        rec = {"file_name": fname, "text": None if cmd == "d" else (text if cmd == "" else cmd)}
        with open(prog_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        break

with open(prog_path, "r", encoding="utf-8") as f:
    kept = [json.loads(l) for l in f if l.strip() and json.loads(l)["text"] is not None]

for fname in {i["file_name"] for i in items} - {r["file_name"] for r in kept}:
    p = os.path.join(base_dir, fname)
    if os.path.exists(p):
        os.remove(p)

with open(path, "w", encoding="utf-8") as f:
    for r in kept:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
os.remove(prog_path)
print(f"Done! Kept {len(kept)} items in {path}.")
