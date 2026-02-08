from pathlib import Path
import subprocess
import sys

def test_pipeline_runs():
    repo = Path(__file__).resolve().parents[1]
    out_md = repo / "data" / "processed" / "ai_summary.md"

    r = subprocess.run([sys.executable, "run_pipeline.py"], cwd=str(repo))
    assert r.returncode == 0
    assert out_md.exists()
    assert out_md.stat().st_size > 100
