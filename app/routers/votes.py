from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

from app.auth import verify_token

router = APIRouter(
    prefix="/candidates",
    tags=["Candidates"],
    dependencies=[Depends(verify_token)]
)


@router.post("/", response_model=schemas.VoteResponse, status_code=201)
def create_vote(vote: schemas.VoteCreate, db: Session = Depends(get_db)):
    return crud.create_vote(db, vote)


@router.get("/", response_model=List[schemas.VoteResponse])
def get_votes(db: Session = Depends(get_db)):
    return crud.get_votes(db)


@router.get("/statistics", response_model=schemas.VoteStatisticsResponse)
def get_vote_statistics(db: Session = Depends(get_db)):
    return crud.get_vote_statistics(db)