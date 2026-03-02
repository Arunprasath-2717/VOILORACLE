"""
VEILORACLE — Main Entry Point
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Usage:
    python main.py pipeline          # Run intelligence pipeline (one-shot)
    python main.py pipeline --loop   # Run pipeline continuously
    python main.py server            # Start FastAPI backend (port 8000)
    python main.py frontend          # Start React frontend (port 5173)
"""

import sys
import logging
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1].lower()

    if command == "pipeline":
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s │ %(name)-28s │ %(levelname)-7s │ %(message)s",
            datefmt="%H:%M:%S",
        )
        from backend.pipeline import run_pipeline
        loop = "--loop" in sys.argv
        run_pipeline(one_shot=not loop)

    elif command == "server":
        print("Starting FastAPI Backend Server on http://localhost:8000")
        subprocess.run([sys.executable, "-m", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"], cwd=str(ROOT))

    elif command == "frontend":
        frontend_dir = ROOT / "frontend"
        print(f"Starting React Frontend Development Server from {frontend_dir}")
        subprocess.run(["npm", "run", "dev"], shell=True, cwd=str(frontend_dir))

    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
