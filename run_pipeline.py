import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent

def run(cmd):
    print(f"[RUN] {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(REPO_ROOT), check=False)
    if r.returncode != 0:
        raise SystemExit(r.returncode)

if __name__ == "__main__":
    run([sys.executable, "detect.py"])
    run([sys.executable, "ai_summarize.py"])
    print("[OK] Pipeline complete.")
    print("Open: data/processed/ai_summary.md")
