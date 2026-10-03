# Architecture

Browser → FastAPI → ffprobe + FFmpeg scene detection + Whisper → OpenCut Model Harness → Qwen/Ollama → Pydantic/deterministic validation → FFmpeg → MP4.

The harness isolates provider-specific model calls from editing logic and constrains the model to JSON. The model cannot execute shell commands.
