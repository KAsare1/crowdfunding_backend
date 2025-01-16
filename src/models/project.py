from datetime import datetime
from pydantic import BaseModel, Field, PositiveInt
from typing import List, Optional



class ProjectBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None
    goal_amount: PositiveInt
    deadline: datetime


class ProjectCreate(ProjectBase):
    pass


class ProjectResponse(ProjectBase):
    id: str
    creator_id: str  
    created_at: datetime
    number_of_contributions: int
    total_contributions: float
    contributors: List[str]

    class Config:
        orm_mode = True

class ProjectListResponse(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    goal_amount: PositiveInt
    deadline: datetime
    creator_id: str
    created_at: datetime
    number_of_contributions: int
    total_contributions: float
    contributor_count: int

    class Config:
        orm_mode = True

