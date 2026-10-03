from backend.app.harness.ollama_qwen import OllamaQwenHarness
from backend.app.models import EditPlan,MediaSummary
from backend.app.config import MAX_OUTPUT_SECONDS
_harness=OllamaQwenHarness()
def generate_plan(brief:str,media:MediaSummary)->EditPlan:return _harness.create_edit_plan(brief,media,MAX_OUTPUT_SECONDS)
