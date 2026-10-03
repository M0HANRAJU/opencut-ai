import json,httpx
from backend.app.config import OLLAMA_BASE_URL,OLLAMA_MODEL,OLLAMA_TIMEOUT_SECONDS
from backend.app.models import EditPlan,MediaSummary
SYSTEM="""You are OpenCut AI's editing planner. Return ONLY JSON matching:
{"title":"string","aspect_ratio":"16:9","segments":[{"source_start":0.0,"source_end":1.0,"reason":"string","caption":null}],"notes":[]}
Use only evidence-backed timestamps; never invent timestamps; preserve coherent thoughts; prefer scene boundaries; max 20 segments; never output commands."""
class OllamaQwenHarness:
    def __init__(self,base_url=OLLAMA_BASE_URL,model=OLLAMA_MODEL): self.url=f"{base_url}/api/chat"; self.model=model
    def create_edit_plan(self,brief,media,max_output_seconds):
        payload={"model":self.model,"stream":False,"format":"json","options":{"temperature":0.1},"messages":[{"role":"system","content":SYSTEM},{"role":"user","content":f"Brief:\n{brief}\nMax duration:{max_output_seconds}\nEvidence:\n{json.dumps(media.model_dump(),ensure_ascii=False)}"}]}
        err=None
        for _ in range(2):
            try:
                r=httpx.post(self.url,json=payload,timeout=OLLAMA_TIMEOUT_SECONDS); r.raise_for_status()
                return EditPlan.model_validate_json(r.json()["message"]["content"])
            except (httpx.HTTPError,KeyError,ValueError) as e: err=e
        raise RuntimeError(f"Model harness failed: {err}")
