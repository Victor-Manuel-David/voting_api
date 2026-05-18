from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError

from app import models, schemas


def create_voter(db: Session, voter: schemas.VoterCreate):
    existing_voter = db.query(models.Voter).filter(
        models.Voter.name == voter.name
    ).first()

    if existing_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Voter is already registered"
        )

    existing_candidate = db.query(models.Candidate).filter(
        models.Candidate.name.ilike(voter.name)
    ).first()

    if existing_candidate:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This person is already registered as a candidate"
        )

    db_voter = models.Voter(
        name=voter.name,
        email=voter.email
    )

    db.add(db_voter)
    db.commit()
    db.refresh(db_voter)

    return db_voter


def get_voters(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    email: str | None = None,
    has_voted: bool | None = None
):
    query = db.query(models.Voter)

    if name:
        query = query.filter(models.Voter.name.ilike(f"%{name}%"))

    if email:
        query = query.filter(models.Voter.email.ilike(f"%{email}%"))

    if has_voted is not None:
        query = query.filter(models.Voter.has_voted == has_voted)

    return query.order_by(models.Voter.id.asc()).offset(skip).limit(limit).all()


def get_voter_by_id(db: Session, voter_id: int):
    voter = db.query(models.Voter).filter(
        models.Voter.id == voter_id
    ).first()

    if not voter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Voter not found"
        )

    return voter


def delete_voter(db: Session, voter_id: int):
    voter = get_voter_by_id(db, voter_id)

    existing_vote = db.query(models.Vote).filter(
        models.Vote.voter_id == voter_id
    ).first()

    if existing_vote:
        candidate = db.query(models.Candidate).filter(
            models.Candidate.id == existing_vote.candidate_id
        ).first()

        if candidate and candidate.votes > 0:
            candidate.votes -= 1

    db.delete(voter)
    db.commit()

    return {
        "message": "Voter deleted successfully"
    }


def create_candidate(db: Session, candidate: schemas.CandidateCreate):
    existing_voter = db.query(models.Voter).filter(
        models.Voter.name.ilike(candidate.name)
    ).first()

    if existing_voter:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This person is already registered as a voter"
        )

    db_candidate = models.Candidate(
        name=candidate.name,
        party=candidate.party
    )

    db.add(db_candidate)
    db.commit()
    db.refresh(db_candidate)

    return db_candidate


def get_candidates(
    db: Session,
    skip: int = 0,
    limit: int = 10,
    name: str | None = None,
    party: str | None = None
):
    query = db.query(models.Candidate)

    if name:
        query = query.filter(models.Candidate.name.ilike(f"%{name}%"))

    if party:
        query = query.filter(models.Candidate.party.ilike(f"%{party}%"))

    return query.order_by(models.Candidate.id.asc()).offset(skip).limit(limit).all()


def get_candidate_by_id(db: Session, candidate_id: int):
    candidate = db.query(models.Candidate).filter(
        models.Candidate.id == candidate_id
    ).first()

    if not candidate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Candidate not found"
        )

    return candidate


def delete_candidate(db: Session, candidate_id: int):
    candidate = get_candidate_by_id(db, candidate_id)

    related_votes = db.query(models.Vote).filter(
        models.Vote.candidate_id == candidate_id
    ).all()

    for vote in related_votes:
        voter = db.query(models.Voter).filter(
            models.Voter.id == vote.voter_id
        ).first()

        if voter:
            voter.has_voted = False

    db.delete(candidate)
    db.commit()

    return {
        "message": "Candidate deleted successfully"
    }


def create_vote(db: Session, vote: schemas.VoteCreate):
    voter = get_voter_by_id(db, vote.voter_id)
    candidate = get_candidate_by_id(db, vote.candidate_id)

    if voter.has_voted:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This voter has already voted"
        )

    db_vote = models.Vote(
        voter_id=vote.voter_id,
        candidate_id=vote.candidate_id
    )

    try:
        voter.has_voted = True
        candidate.votes += 1

        db.add(db_vote)
        db.commit()
        db.refresh(db_vote)

        return db_vote

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This voter has already voted"
        )


def get_votes(db: Session):
    return db.query(models.Vote).order_by(models.Vote.id.asc()).all()


def get_vote_statistics(db: Session):
    total_votes = db.query(models.Vote).count()

    total_voters_who_voted = db.query(models.Voter).filter(
        models.Voter.has_voted == True
    ).count()

    candidates = db.query(models.Candidate).order_by(
        models.Candidate.votes.desc(),
        models.Candidate.id.asc()
    ).all()

    results = []

    for candidate in candidates:
        percentage = 0

        if total_votes > 0:
            percentage = round((candidate.votes / total_votes) * 100, 2)

        results.append({
            "candidate_id": candidate.id,
            "candidate_name": candidate.name,
            "party": candidate.party,
            "votes": candidate.votes,
            "percentage": percentage
        })

    return {
        "total_votes": total_votes,
        "total_voters_who_voted": total_voters_who_voted,
        "results": results
    }