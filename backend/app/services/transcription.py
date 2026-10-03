from pathlib import Path
import whisper
_model=None
def transcribe(path:Path)->list[dict]:
    global _model
    if _model is None:_model=whisper.load_model("turbo")
    r=_model.transcribe(str(path),fp16=False)
    return [{"start":float(s["start"]),"end":float(s["end"]),"text":s["text"].strip()} for s in r.get("segments",[]) if float(s["end"])>float(s["start"])]
