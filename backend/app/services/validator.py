from backend.app.config import MAX_OUTPUT_SECONDS
from backend.app.models import EditPlan,MediaSummary
def validate_plan(plan:EditPlan,media:MediaSummary)->EditPlan:
    kept=[]; total=0.0
    for s in plan.segments:
        a=max(0,min(float(s.source_start),media.duration)); b=max(0,min(float(s.source_end),media.duration))
        if b<=a or b-a<.15:continue
        remain=MAX_OUTPUT_SECONDS-total
        if remain<=0:break
        b=min(b,a+remain); kept.append(s.model_copy(update={"source_start":round(a,3),"source_end":round(b,3)})); total+=b-a
    if not kept:raise ValueError("No valid edit segments remained after validation")
    return plan.model_copy(update={"segments":kept})
