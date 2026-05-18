from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import crud, schemas
from app.database import get_db

from app.auth import verify_token

router = APIRouter(
    prefix="/voters",
    tags=["Voters"],
    dependencies=[Depends(verify_token)]
)


@router.post("/", response_model=schemas.VoterResponse, status_code=201)
def create_voter(voter: schemas.VoterCreate, db: Session = Depends(get_db)):
    return crud.create_voter(db, voter)


@router.get("/", response_model=List[schemas.VoterResponse])
def get_voters(db: Session = Depends(get_db)):
    return crud.get_voters(db)


@router.get("/{voter_id}", response_model=schemas.VoterResponse)
def get_voter_by_id(voter_id: int, db: Session = Depends(get_db)):
    return crud.get_voter_by_id(db, voter_id)


@router.delete("/{voter_id}")
def delete_voter(voter_id: int, db: Session = Depends(get_db)):
    return crud.delete_voter(db, voter_id)