# FastAPI Artist Directory API

A lightweight RESTful API built with **FastAPI** for browsing a directory of music artists, with filtering by genre, album ownership, and name search.

## Features

- Typed request/response schemas defined with **Pydantic**
- Enum-restricted genre filtering (`romantic`, `rap`)
- Query-parameter filtering by genre, album presence, and name search (`/singers?genre=rap&has_album=true&q=amr`)
- Path-parameter validation (e.g., singer ID must be ≥ 1)
- Custom Pydantic field validator that normalizes genre casing on creation
- Structured `HTTPException` handling for 404 responses

## Tech Stack

- Python 3.8+
- FastAPI 0.103.2
- Pydantic 2.5.3
- Uvicorn 0.22.0

## Endpoints

| Method | Endpoint              | Description                                              |
|--------|------------------------|------------------------------------------------------------|
| GET    | `/`                    | Health check                                                |
| GET    | `/about`               | About this API                                              |
| GET    | `/singers`             | List singers — filter by `genre`, `has_album`, `q` (name search) |
| GET    | `/singers/{singer_id}` | Get a single singer by ID                                   |
| POST   | `/singers`             | Add a new singer                                            |

## Setup

```bash
git clone https://github.com/elm0hamady/FastAPI-Artist-Directory-API-.git
cd FastAPI-Artist-Directory-API-

python -m venv venv
source venv/bin/activate      # venv\Scripts\activate on Windows

pip install -r requirements.txt
uvicorn main:app --reload
```

Interactive API docs are then available at `http://127.0.0.1:8000/docs`.

## Notes

Artist data currently lives in an in-memory Python list rather than a database — persisting it via SQLAlchemy (or a similar ORM) is a natural next step.
