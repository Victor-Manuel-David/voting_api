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

@router.post("/", response_model=schemas.CandidateResponse, status_code=201)
def create_candidate(candidate: schemas.CandidateCreate, db: Session = Depends(get_db)):
    return crud.create_candidate(db, candidate)


@router.get("/", response_model=List[schemas.CandidateResponse])
def get_candidates(db: Session = Depends(get_db)):
    return crud.get_candidates(db)


@router.get("/{candidate_id}", response_model=schemas.CandidateResponse)
def get_candidate_by_id(candidate_id: int, db: Session = Depends(get_db)):
    return crud.get_candidate_by_id(db, candidate_id)


@router.delete("/{candidate_id}")
def delete_candidate(candidate_id: int, db: Session = Depends(get_db)):
    return crud.delete_candidate(db, candidate_id)