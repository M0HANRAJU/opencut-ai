import uuid
from pathlib import Path
from fastapi import FastAPI,File,Form,HTTPException,UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from backend.app.config import STORAGE_DIR,MAX_UPLOAD_MB
from backend.app.models import MediaSummary,Project
from backend.app.services.video import probe,detect_scenes
from backend.app.services.transcription import transcribe
from backend.app.services.planner import generate_plan
from backend.app.services.validator import validate_plan
from backend.app.services.renderer import render
app=FastAPI(title="OpenCut AI",version="0.1.0")
app.add_middleware(CORSMiddleware,allow_origins=["http://localhost:5173"],allow_methods=["*"],allow_headers=["*"])
app.mount("/media",StaticFiles(directory=STORAGE_DIR),name="media")
projects={}
@app.get("/api/health")
def health():return {"ok":True}
@app.post("/api/projects",response_model=Project)
async def create_project(file:UploadFile=File(...)):
    suffix=Path(file.filename or "").suffix.lower()
    if suffix not in {".mp4",".mov",".webm",".mkv",".m4v"}:raise HTTPException(400,"Unsupported video format")
    pid=uuid.uuid4().hex; d=STORAGE_DIR/pid; d.mkdir(parents=True,exist_ok=True); src=d/Path(file.filename or "source.mp4").name
    size=0
    with src.open("wb") as out:
        while chunk:=await file.read(1024*1024):
            size+=len(chunk)
            if size>MAX_UPLOAD_MB*1024*1024:src.unlink(missing_ok=True);raise HTTPException(413,"Upload exceeds configured limit")
            out.write(chunk)
    try:
        meta=probe(src); media=MediaSummary(**meta,scenes=detect_scenes(src,meta["duration"]),transcript=transcribe(src))
    except Exception as e:src.unlink(missing_ok=True);raise HTTPException(500,f"Media analysis failed: {e}") from e
    p=Project(id=pid,filename=src.name,media=media);projects[pid]=p;return p
@app.post("/api/projects/{pid}/plan",response_model=Project)
async def plan_project(pid:str,brief:str=Form(...)):
    p=projects.get(pid)
    if not p:raise HTTPException(404,"Project not found")
    try:p.plan=validate_plan(generate_plan(brief.strip(),p.media),p.media)
    except Exception as e:raise HTTPException(502,f"Planning failed: {e}") from e
    return p
@app.post("/api/projects/{pid}/render",response_model=Project)
def render_project(pid:str):
    p=projects.get(pid)
    if not p or not p.plan:raise HTTPException(400,"Generate a plan first")
    try:o=render(STORAGE_DIR/pid/p.filename,pid,p.plan)
    except Exception as e:raise HTTPException(500,f"Render failed: {e}") from e
    p.rendered_file=f"/media/{pid}/renders/{o.name}";return p
@app.get("/api/projects/{pid}",response_model=Project)
def get_project(pid:str):
    p=projects.get(pid)
    if not p:raise HTTPException(404,"Project not found")
    return p
