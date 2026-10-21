from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from exceptions import NoteError, NoteNotFoundError, DuplicateTitleError, EmptyUpdateError

async def note_error_handler(request: Request, exc: NoteError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

async def note_not_found_handler(request: Request, exc: NoteNotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})

async def duplicate_title_handler(request: Request, exc: DuplicateTitleError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})

async def empty_update_handler(request: Request, exc: EmptyUpdateError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})

def register_handlers(app: FastAPI):
    app.add_exception_handler(NoteError, note_error_handler)
    app.add_exception_handler(NoteNotFoundError, note_not_found_handler)
    app.add_exception_handler(DuplicateTitleError, duplicate_title_handler)
    app.add_exception_handler(EmptyUpdateError, empty_update_handler)
