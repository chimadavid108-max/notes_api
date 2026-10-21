from sqlalchemy import func, or_
from sqlalchemy.orm import Session
from exceptions import DuplicateTitleError, EmptyUpdateError, NoteNotFoundError
from models import Note
from schemas import NoteCreate, NoteUpdate


def get_note(db: Session, note_id: int) -> Note:
    note = db.get(Note, note_id)
    if note is None:
        raise NoteNotFoundError(note_id)
    return note


def ensure_title_available(db: Session, title: str, exclude_id: int | None = None) -> None:
    query = db.query(Note).filter(func.lower(Note.title) == title.lower())
    if exclude_id is not None:
        query = query.filter(Note.id != exclude_id)
    if query.first() is not None:
        raise DuplicateTitleError(title)


def create_note(db: Session, data: NoteCreate) -> Note:
    ensure_title_available(db, data.title)
    note = Note(**data.model_dump())
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def list_notes(db: Session, q: str | None = None, category: str | None = None,
               pinned: bool | None = None, limit: int = 10, offset: int = 0) -> list[Note]:
    query = db.query(Note)
    if q is not None:
        pattern = f"%{q}%"
        query = query.filter(or_(Note.title.ilike(pattern), Note.content.ilike(pattern)))
    if category is not None:
        query = query.filter(Note.category == category)
    if pinned is not None:
        query = query.filter(Note.pinned == pinned)
    return (
        query.order_by(Note.pinned.desc(), Note.created_at.desc(), Note.id.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


def update_note(db: Session, note_id: int, data: NoteUpdate) -> Note:
    note = get_note(db, note_id)
    updates = data.model_dump(exclude_unset=True)
    if not updates:
        raise EmptyUpdateError("No fields to update. Send at least one field.")
    if "title" in updates:
        ensure_title_available(db, updates["title"], exclude_id=note_id)
    for field, value in updates.items():
        setattr(note, field, value)
    db.commit()
    db.refresh(note)
    return note


def delete_note(db: Session, note_id: int) -> None:
    note = get_note(db, note_id)
    db.delete(note)
    db.commit()
