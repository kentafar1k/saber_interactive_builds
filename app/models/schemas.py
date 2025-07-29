from typing import List, Dict, Optional
from pydantic import BaseModel, Field

class Task(BaseModel):
    name: str
    dependencies: List[str] = Field(default_factory=list)

class Build(BaseModel):
    name: str
    tasks: List[str]

class BuildRequest(BaseModel):
    build: str

class ErrorResponse(BaseModel):
    detail: str 