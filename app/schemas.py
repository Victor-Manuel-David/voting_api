from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, ConfigDict, Field


class VoterBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr


class VoterCreate(VoterBase):
    pass


class VoterResponse(VoterBase):
    id: int
    has_voted: bool

    model_config = ConfigDict(from_attributes=True)


class CandidateBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    party: Optional[str] = Field(default=None, max_length=100)


class CandidateCreate(CandidateBase):
    pass


class CandidateResponse(CandidateBase):
    id: int
    votes: int

    model_config = ConfigDict(from_attributes=True)


class VoteCreate(BaseModel):
    voter_id: int
    candidate_id: int


class VoteResponse(BaseModel):
    id: int
    voter_id: int
    candidate_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CandidateStatistics(BaseModel):
    candidate_id: int
    candidate_name: str
    party: Optional[str]
    votes: int
    percentage: float


class VoteStatisticsResponse(BaseModel):
    total_votes: int
    total_voters_who_voted: int
    results: List[CandidateStatistics]