from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Voter(Base):
    __tablename__ = "voters"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False, index=True)
    has_voted = Column(Boolean, default=False, nullable=False)

    vote = relationship("Vote", back_populates="voter", cascade="all, delete-orphan", uselist=False)


class Candidate(Base):
    __tablename__ = "candidates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    party = Column(String(100), nullable=True)
    votes = Column(Integer, default=0, nullable=False)

    votes_relation = relationship("Vote", back_populates="candidate", cascade="all, delete-orphan")


class Vote(Base):
    __tablename__ = "votes"

    id = Column(Integer, primary_key=True, index=True)
    voter_id = Column(Integer, ForeignKey("voters.id", ondelete="CASCADE"), unique=True, nullable=False)
    candidate_id = Column(Integer, ForeignKey("candidates.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    voter = relationship("Voter", back_populates="vote")
    candidate = relationship("Candidate", back_populates="votes_relation")