"""Download the tested public Qwen model into this checkout (optional)."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for name, folder in (("HF_HOME", "cache/huggingface"), ("TEMP", "tmp"), ("TMP", "tmp")):
    path = ROOT / folder
    path.mkdir(parents=True, exist_ok=True)
    os.environ[name] = str(path)
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"
from huggingface_hub import snapshot_download

REPO = "Qwen/Qwen3-TTS-12Hz-0.6B-Base"
REVISION = "5d83992436eae1d760afd27aff78a71d676296fc"

if __name__ == "__main__":
    target = ROOT / "models" / REPO.split("/")[-1]
    print(f"Downloading {REPO}@{REVISION} into {target}", flush=True)
    snapshot_download(repo_id=REPO, revision=REVISION, local_dir=str(target))
    print("Model download complete.", flush=True)
