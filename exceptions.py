class NoteError(Exception):
    pass


class NoteNotFoundError(NoteError):
    def __init__(self, note_id: int) -> None:
        self.note_id = note_id
        super().__init__(f"Note with ID {self.note_id} not found")


class DuplicateTitleError(NoteError):
    def __init__(self, title: str) -> None:
        self.title = title
        super().__init__(f"A note titled '{self.title}' already exists.")


class EmptyUpdateError(NoteError):
    pass
