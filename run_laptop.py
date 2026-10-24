"""Start a localhost-only Streamlit desk with direct phone sync enabled."""
import os
import subprocess
import sys
from pathlib import Path

os.environ["SYSTEM_LAN_SYNC"] = "1"
subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
                "--server.address=127.0.0.1"], cwd=Path(__file__).resolve().parent, check=True)
