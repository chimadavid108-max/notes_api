from fastapi import FastAPI
from config import APP_NAME
from database import Base, engine
from handlers import register_handlers
from routers.notes import router as note_router

Base.metadata.create_all(engine)
app = FastAPI()

app.include_router(note_router)
register_handlers(app)


@app.get("/")
def root():
    return {"message": f"{APP_NAME} is running"}


@app.get("/health")
def status():
    return {"status": "ok"}
