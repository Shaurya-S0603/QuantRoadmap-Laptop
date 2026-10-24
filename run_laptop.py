"""Optionally run the standalone study site on localhost."""
import subprocess
import sys
from pathlib import Path

subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
                "--server.address=127.0.0.1"], cwd=Path(__file__).resolve().parent, check=True)
