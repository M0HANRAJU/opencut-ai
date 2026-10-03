import json,re,subprocess
from pathlib import Path
def probe(path:Path)->dict:
    r=subprocess.run(["ffprobe","-v","error","-print_format","json","-show_streams","-show_format",str(path)],capture_output=True,text=True,check=True)
    d=json.loads(r.stdout); v=next(s for s in d["streams"] if s.get("codec_type")=="video"); n=v.get("r_frame_rate","30/1").split("/")
    return {"duration":float(d["format"].get("duration",0)),"width":int(v["width"]),"height":int(v["height"]),"fps":float(n[0])/float(n[1] or 1)}
def detect_scenes(path:Path,duration:float)->list[dict]:
    r=subprocess.run(["ffmpeg","-hide_banner","-i",str(path),"-vf","select='gt(scene,0.35)',showinfo","-an","-f","null","-"],capture_output=True,text=True)
    points=[0.0]+[float(m.group(1)) for m in re.finditer(r"pts_time:([0-9.]+)",r.stderr) if 0<float(m.group(1))<duration]+[duration]
    points=sorted(set(points)); return [{"start":points[i],"end":points[i+1],"score":0.0} for i in range(len(points)-1) if points[i+1]>points[i]]
