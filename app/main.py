from fastapi import FastAPI

from app.database import Base, engine
from app.routers import voters, candidates, votes, auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Voting API",
    description="REST API for managing voters, candidates and votes."
)


@app.get("/")
def root():
    return {
        "message": "Voting API is running"
    }


app.include_router(auth.router)
app.include_router(voters.router)
app.include_router(candidates.router)
app.include_router(votes.router)