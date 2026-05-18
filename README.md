# Voting API

REST API developed with **FastAPI**, **PostgreSQL**, **SQLAlchemy** and **JWT authentication** for managing a voting system.

This project allows the registration of voters and candidates, vote casting, vote validation, result statistics, filtering and pagination. Each voter can vote only once, and the system prevents a person from being registered as both voter and candidate.

---

## Technologies Used

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
- Filter voters by name, email and voting status.
- Paginate voters list.
- Get voter details by ID.
- Delete voters.
- Register candidates.
- List candidates.
- Filter candidates by name and political party.
- Paginate candidates list.
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
```

---

## Database Model

The system uses three main tables: `voters`, `candidates` and `votes`.

### Voters

| Field | Type | Description |
|---|---|---|
| id | integer | Unique voter ID |
| name | string | Voter name |
| email | string | Unique voter email |
| has_voted | boolean | Indicates if the voter has already voted |

### Candidates

| Field | Type | Description |
|---|---|---|
| id | integer | Unique candidate ID |
| name | string | Candidate name |
| party | string | Political party |
| votes | integer | Number of votes received |

### Votes

| Field | Type | Description |
|---|---|---|
| id | integer | Unique vote ID |
| voter_id | integer | Related voter ID |
| candidate_id | integer | Related candidate ID |
| created_at | timestamp | Vote creation date |

---

## Database Script

```sql
CREATE TABLE voters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    has_voted BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    party VARCHAR(100),
    votes INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE votes (
    id SERIAL PRIMARY KEY,
    voter_id INTEGER NOT NULL UNIQUE,
    candidate_id INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vote_voter
        FOREIGN KEY (voter_id)
        REFERENCES voters(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_vote_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES candidates(id)
        ON DELETE CASCADE
);
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Victor-Manuel-David/voting-api.git
cd voting-api
```

---

### 2. Create a virtual environment

```bash
py -m venv venv
```

---

### 3. Activate the virtual environment

On Windows:

```bash
venv\Scripts\activate
```

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the root folder and add the following configuration:

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=voting_db
DB_USER=postgres
DB_PASSWORD=your_password

SECRET_KEY=super_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Replace `your_password` with your PostgreSQL password.

Important: the `.env` file must not be uploaded to GitHub.

---

## Run the Project

Run the API with:

```bash
uvicorn app.main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

Swagger documentation will be available at:

```text
http://127.0.0.1:8000/docs
```

---

## Authentication

The API uses JWT authentication to protect the main endpoints.

### Login Credentials

```text
username: admin
password: admin123
```

### Login Endpoint

```http
POST /auth/login
```

In Swagger, click the **Authorize** button and enter:

```text
username: admin
password: admin123
```

After authorization, the protected endpoints can be used.

---

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/login` | Generate JWT access token |

---

### Voters

| Method | Endpoint | Description |
|---|---|---|
| POST | `/voters/` | Register a new voter |
| GET | `/voters/` | Get all voters with filtering and pagination |
| GET | `/voters/{voter_id}` | Get voter by ID |
| DELETE | `/voters/{voter_id}` | Delete voter |

---

### Candidates

| Method | Endpoint | Description |
|---|---|---|
| POST | `/candidates/` | Register a new candidate |
| GET | `/candidates/` | Get all candidates with filtering and pagination |
| GET | `/candidates/{candidate_id}` | Get candidate by ID |
| DELETE | `/candidates/{candidate_id}` | Delete candidate |

---

### Votes

| Method | Endpoint | Description |
|---|---|---|
| POST | `/votes/` | Cast a vote |
| GET | `/votes/` | Get all votes |
| GET | `/votes/statistics` | Get voting statistics |

---

## Filtering and Pagination

The voters and candidates list endpoints support filtering and pagination using query parameters.

---

### Voters Filtering and Pagination

Endpoint:

```http
GET /voters/
```

Available query parameters:

| Parameter | Type | Description |
|---|---|---|
| skip | integer | Number of records to skip |
| limit | integer | Maximum number of records to return |
| name | string | Filter voters by name |
| email | string | Filter voters by email |
| has_voted | boolean | Filter voters by voting status |

Examples:

```http
GET /voters/?skip=0&limit=10
```

```http
GET /voters/?name=ana
```

```http
GET /voters/?email=example
```

```http
GET /voters/?has_voted=true
```

```http
GET /voters/?name=ana&skip=0&limit=5
```

---

### Candidates Filtering and Pagination

Endpoint:

```http
GET /candidates/
```

Available query parameters:

| Parameter | Type | Description |
|---|---|---|
| skip | integer | Number of records to skip |
| limit | integer | Maximum number of records to return |
| name | string | Filter candidates by name |
| party | string | Filter candidates by political party |

Examples:

```http
GET /candidates/?skip=0&limit=10
```

```http
GET /candidates/?name=carlos
```

```http
GET /candidates/?party=azul
```

```http
GET /candidates/?name=carlos&party=azul&skip=0&limit=5
```

---

## Request Examples

### Create a Voter

```http
POST /voters/
```

Request body:

```json
{
  "name": "Ana Perez",
  "email": "ana@example.com"
}
```

Response example:

```json
{
  "name": "Ana Perez",
  "email": "ana@example.com",
  "id": 1,
  "has_voted": false
}
```

---

### Create a Candidate

```http
POST /candidates/
```

Request body:

```json
{
  "name": "Carlos Gomez",
  "party": "Partido Azul"
}
```

Response example:

```json
{
  "name": "Carlos Gomez",
  "party": "Partido Azul",
  "id": 1,
  "votes": 0
}
```

---

### Cast a Vote

```http
POST /votes/
```

Request body:

```json
{
  "voter_id": 1,
  "candidate_id": 1
}
```

Response example:

```json
{
  "id": 1,
  "voter_id": 1,
  "candidate_id": 1,
  "created_at": "2026-05-17T10:30:00"
}
```

---

## Statistics Response Example

Endpoint:

```http
GET /votes/statistics
```

Response example:

```json
{
  "total_votes": 1,
  "total_voters_who_voted": 1,
  "results": [
    {
      "candidate_id": 1,
      "candidate_name": "Carlos Gomez",
      "party": "Partido Azul",
      "votes": 1,
      "percentage": 100.0
    }
  ]
}
```

---

## cURL Examples

### Login

```bash
curl -X POST "http://127.0.0.1:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"
```

---

### Create a Voter

Replace `YOUR_TOKEN` with the JWT access token.

```bash
curl -X POST "http://127.0.0.1:8000/voters/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Ana Perez\",\"email\":\"ana@example.com\"}"
```

---

### Create a Candidate

```bash
curl -X POST "http://127.0.0.1:8000/candidates/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"Carlos Gomez\",\"party\":\"Partido Azul\"}"
```

---

### Cast a Vote

```bash
curl -X POST "http://127.0.0.1:8000/votes/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"voter_id\":1,\"candidate_id\":1}"
```

---

### Get Voting Statistics

```bash
curl -X GET "http://127.0.0.1:8000/votes/statistics" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Get Voters with Filtering and Pagination

```bash
curl -X GET "http://127.0.0.1:8000/voters/?skip=0&limit=10&name=ana" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

### Get Candidates with Filtering and Pagination

```bash
curl -X GET "http://127.0.0.1:8000/candidates/?skip=0&limit=10&party=azul" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Validations Implemented

The system includes the following validations:

- A voter cannot vote more than once.
- A voter cannot be registered as a candidate.
- A candidate cannot be registered as a voter.
- A voter email must be unique.
- A vote can only be cast if the voter exists.
- A vote can only be cast if the candidate exists.
- The `has_voted` field is automatically updated after voting.
- The candidate vote count is automatically incremented.
- Protected endpoints require JWT authentication.
- Pagination parameters are validated.
- Filtering is available for voters and candidates.

---

## Error Examples

### Invalid Login

```json
{
  "detail": "Invalid username or password"
}
```

---

### Not Authenticated

```json
{
  "detail": "Not authenticated"
}
```

---

### Invalid or Expired Token

```json
{
  "detail": "Invalid or expired authentication token"
}
```

---

### Voter Already Voted

```json
{
  "detail": "This voter has already voted"
}
```

---

### Voter Not Found

```json
{
  "detail": "Voter not found"
}
```

---

### Candidate Not Found

```json
{
  "detail": "Candidate not found"
}
```

---

### Email Already Registered

```json
{
  "detail": "Email is already registered"
}
```

---

### Voter Already Registered as Candidate

```json
{
  "detail": "This person is already registered as a candidate"
}
```

---

### Candidate Already Registered as Voter

```json
{
  "detail": "This person is already registered as a voter"
}
```

---

## Swagger Documentation

FastAPI automatically generates Swagger documentation using the OpenAPI standard.

Once the project is running, open:

```text
http://127.0.0.1:8000/docs
```

Swagger allows testing the endpoints directly from the browser.

---


## Notes

For this technical test, JWT authentication uses fixed admin credentials:

```text
username: admin
password: admin123
```

In a production environment, this should be improved by adding:

- Users table.
- Hashed passwords.
- Role-based access control.
- Refresh tokens.
- Stronger secret key management.

---

## Author VICTOR MANUEL DAVID RODRIGUEZ

Developed as a technical test for a Software Developer position.