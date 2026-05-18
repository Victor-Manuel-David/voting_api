# Voting API

REST API developed with **FastAPI**, **PostgreSQL** and **JWT authentication** for managing a voting system.

This project allows the registration of voters and candidates, vote casting, vote validation, and result statistics. Each voter can vote only once, and the system prevents a person from being registered as both voter and candidate at the same time.

---

## Technologies Used In this Project

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- JWT Authentication
- Uvicorn
- Swagger / OpenAPI

---

## Project Features

- Register voters.
- List voters.
- Get voter details by ID.
- Delete voters.
- Register candidates.
- List candidates.
- Get candidate details by ID.
- Delete candidates.
- Cast votes.
- List all votes.
- Get voting statistics.
- Prevent duplicate votes.
- Prevent a voter from being registered as a candidate and vice versa.
- Automatically update the voter status after voting.
- Automatically increase the candidate vote count.
- Protect endpoints using JWT authentication.
- API documentation with Swagger.

---

## Project Structure

```text
voting_api/
│
├── app/
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── candidates.py
│   │   ├── voters.py
│   │   └── vote.py
│   │
│   ├── __init__.py
│   ├── auth.py
│   ├── crud.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── venv/
├── .env
├── .gitignore
├── README.md
└── requirements.txt