# OpenCut AI

OpenCut AI is a local-first, open-source AI video editing assistant. Describe the edit you want; OpenCut analyzes the source, transcribes speech with Whisper, asks a local Qwen model for a structured edit decision list, validates every timestamp deterministically, and renders the result with FFmpeg.

## Architecture

```
Video
  ↓
ffprobe + FFmpeg scene detection + Whisper
  ↓
Media evidence
  ↓
Original OpenCut Model Harness
  ↓
Qwen via Ollama
  ↓
Structured JSON edit plan
  ↓
Pydantic + deterministic timeline validation
  ↓
FFmpeg
  ↓
Edited MP4
```

The model is an important part of the editing workflow, but it never executes shell commands. Its output is untrusted data.

## Requirements

- Python 3.11+
- Node.js 20+
- FFmpeg and ffprobe
- Ollama
- A compatible Qwen2.5 model

Pull the default model:

```bash
ollama pull qwen2.5:7b
```

## Run the backend

```bash
cd backend
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## Run the frontend

In another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

## Demo flow

1. Choose a video.
2. Click **Analyze video**.
3. Describe the desired edit.
4. Click **Generate AI edit**.
5. Review the timestamped plan.
6. Click **Render**.
7. Preview the resulting MP4.

## Repository structure

- `.agents/skills/video-editing/` — Agent Skill following the open Agent Skills convention.
- `backend/app/harness/` — original provider-isolated model harness.
- `backend/app/services/` — media analysis, planning, validation and rendering.
- `frontend/` — React/Vite interface.
- `tests/` — validation and harness tests.
- `.github/workflows/ci.yml` — backend and frontend CI.

## Challenge alignment

Open-source/open-weight AI is central to the product: Whisper supplies speech evidence and a locally served Qwen model performs natural-language editing-plan reasoning. The repository also contains an original model-harness implementation and an Agent Skill.

## Security

AI output is never treated as executable code. Timeline validation clamps timestamps to the source duration and enforces output-duration and segment-count limits. Production deployments should add authentication, isolated render workers, persistent storage, rate limiting and stricter upload/resource controls.

## License

MIT. Third-party software and model variants retain their respective licenses. Model weights are not bundled in this repository.
