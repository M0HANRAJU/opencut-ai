from pathlib import Path
import os
BASE_DIR=Path(__file__).resolve().parents[1]
STORAGE_DIR=BASE_DIR/"storage"; STORAGE_DIR.mkdir(parents=True,exist_ok=True)
OLLAMA_BASE_URL=os.getenv("OLLAMA_BASE_URL","http://localhost:11434").rstrip("/")
OLLAMA_MODEL=os.getenv("OLLAMA_MODEL","qwen2.5:7b")
OLLAMA_TIMEOUT_SECONDS=int(os.getenv("OLLAMA_TIMEOUT_SECONDS","120"))
MAX_UPLOAD_MB=int(os.getenv("MAX_UPLOAD_MB","1024"))
MAX_OUTPUT_SECONDS=float(os.getenv("MAX_OUTPUT_SECONDS","60"))
