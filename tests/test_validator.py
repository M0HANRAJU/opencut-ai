from backend.app.models import EditPlan,EditSegment,MediaSummary
from backend.app.services.validator import validate_plan
def test_clamps(): 
    m=MediaSummary(duration=10,width=1920,height=1080,fps=30);p=EditPlan(title="x",segments=[EditSegment(source_start=-2,source_end=4)])
    o=validate_plan(p,m);assert o.segments[0].source_start==0
def test_rejects_tiny():
    m=MediaSummary(duration=10,width=1920,height=1080,fps=30);p=EditPlan(title="x",segments=[EditSegment(source_start=1,source_end=1.05)])
    try:validate_plan(p,m);assert False
    except ValueError:assert True
