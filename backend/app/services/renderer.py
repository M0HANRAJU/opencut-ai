import uuid,subprocess
from pathlib import Path
from backend.app.config import STORAGE_DIR
from backend.app.models import EditPlan
def render(source:Path,project_id:str,plan:EditPlan)->Path:
    out=STORAGE_DIR/project_id/"renders"; out.mkdir(parents=True,exist_ok=True); target=out/f"{uuid.uuid4().hex}.mp4"
    args=["ffmpeg","-y","-hide_banner"]; filt=[] 
    for i,s in enumerate(plan.segments):
        args+=["-ss",str(s.source_start),"-to",str(s.source_end),"-i",str(source)]
        filt.append(f"[{i}:v]setpts=PTS-STARTPTS[v{i}];[{i}:a]asetpts=PTS-STARTPTS[a{i}]")
    ins="".join(f"[v{i}][a{i}]" for i in range(len(plan.segments)))
    filt.append(f"{ins}concat=n={len(plan.segments)}:v=1:a=1[v][a]")
    subprocess.run(args+["-filter_complex",";".join(filt),"-map","[v]","-map","[a]","-c:v","libx264","-crf","20","-c:a","aac","-movflags","+faststart",str(target)],check=True,capture_output=True,text=True)
    return target
