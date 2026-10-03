from typing import Protocol
from backend.app.models import EditPlan,MediaSummary
class ModelHarness(Protocol):
    def create_edit_plan(self,brief:str,media:MediaSummary,max_output_seconds:float)->EditPlan: ...
