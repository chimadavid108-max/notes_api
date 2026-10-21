from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.orm import Session
import crud
from config import LIST_LIMIT
from database import get_db
from schemas import NoteCreate, NoteOut, NoteUpdate

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("", response_model=list[NoteOut])
def get_all_notes(
    q: str | None = None,
    category: str | None = None,
    pinned: bool | None = None,
    limit: int = Query(LIST_LIMIT, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    return crud.list_notes(db, q, category, pinned, limit, offset)


@router.get("/{note_id}", response_model=NoteOut)
def find_note(note_id: int, db: Session = Depends(get_db)):
    return crud.get_note(db, note_id)


@router.post("", status_code=201, response_model=NoteOut)
def add_note(data: NoteCreate, db: Session = Depends(get_db)):
    return crud.create_note(db, data)


@router.patch("/{note_id}", response_model=NoteOut)
def update(note_id: int, data: NoteUpdate, db: Session = Depends(get_db)):
    return crud.update_note(db, note_id, data)


@router.delete("/{note_id}", status_code=204)
def remove_note(note_id: int, db: Session = Depends(get_db)):
    crud.delete_note(db, note_id)
    return Response(status_code=204)
