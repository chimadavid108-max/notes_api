# 💻 Notes API
A CRUD notes API built in Python, and has good project architecture. Create, list, find, update and delete notes using HTTP request.
It stores the note in database via sqlalchemy.

## ✨ Features
- It was built with FastAPI module.
- Pure functions.
- Error handling for both python and the route.
- Uses Pydantic for input validation.
- You can post notes (Saved in notes.db).
- View all notes.
- Pin notes.
- List notes — It can be sorted by keyword searching, pinned, and date.
- ID is autoincremented.
- All status can be updated.
- It has .env configuration.
- Status codes are specific.


## 🛠️Tech stack
- Python 
- Pydantic
- SQLAlchemy
- FastAPI
- Database

## Project Structure
```text
notes_api/
├── main.py
├── config.py
├── database.py
├── exceptions.py
├── models.py          ← SQLAlchemy table
├── schemas.py         ← Pydantic models (in/out of the API)
├── crud.py            ← core logic: all DB work, raises domain exceptions
├── handlers.py        ← exception → HTTP response
├── routers/
│   ├── __init__.py
│   └── notes.py       ← the /notes routes
├── requirements.txt
├── .gitignore
└── README.md

```

## Start Using
1. **Clone the repository**
```bash
git  clone https://github.com/chimadavid108-max/notes_api.git
cd notes_api/
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the API**
```bash
uvicorn main:app --reload
```

### FREE TO USE AND MODIFY
