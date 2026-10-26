import pytest
from crud import create_note, ensure_title_available, get_note
from exceptions import DuplicateTitleError, NoteNotFoundError
from schemas import NoteCreate


def test_get_note_raises_when_missing(db_session):
    with pytest.raises(NoteNotFoundError):
        get_note(db_session, 12345)


def test_ensure_title_available_is_case_insensitive(db_session):
    create_note(db_session, NoteCreate(title="ideas", content="x"))
    with pytest.raises(DuplicateTitleError):
        ensure_title_available(db_session, "IDEAS")


def test_ensure_title_available_excludes_own_id(db_session):
    note = create_note(db_session, NoteCreate(title="ideas", content="x"))
    assert ensure_title_available(db_session, "ideas", exclude_id=note.id) is None
