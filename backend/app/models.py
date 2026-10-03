from typing import Literal
from pydantic import BaseModel,Field
class TranscriptSegment(BaseModel):
    start:float=Field(ge=0); end:float=Field(gt=0); text:str
class Scene(BaseModel):
    start:float=Field(ge=0); end:float=Field(gt=0); score:float=0
class MediaSummary(BaseModel):
    duration:float=Field(ge=0); width:int=Field(gt=0); height:int=Field(gt=0); fps:float=Field(gt=0)
    scenes:list[Scene]=[]; transcript:list[TranscriptSegment]=[]
class EditSegment(BaseModel):
    source_start:float=Field(ge=0); source_end:float=Field(gt=0); reason:str=""; caption:str|None=None
class EditPlan(BaseModel):
    title:str; aspect_ratio:Literal["16:9","9:16","1:1"]="16:9"
    segments:list[EditSegment]=Field(min_length=1,max_length=20); notes:list[str]=[]
class Project(BaseModel):
    id:str; filename:str; media:MediaSummary; plan:EditPlan|None=None; rendered_file:str|None=None
