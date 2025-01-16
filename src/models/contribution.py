from datetime import datetime
from pydantic import BaseModel, PositiveInt


class ContributionBase(BaseModel):
    amount: PositiveInt


class ContributionCreate(ContributionBase):
    project_id: str


class ContributorDetails(BaseModel):
    id: str
    username: str
    email: str

    class Config:
        orm_mode = True

class ContributionResponse(BaseModel):
    id: int
    amount: PositiveInt
    contributed_at: datetime
    project_id: str
    contributor: ContributorDetails

    class Config:
        orm_mode = True