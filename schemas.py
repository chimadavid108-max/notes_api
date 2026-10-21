from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, field_validator


def _strip(value):
    return value.strip() if isinstance(value, str) else value


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1, max_length=5000)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    pinned: bool = False

    @field_validator("title", "content", "category", mode="before")
    @classmethod
    def strip_text(cls, value):
        return _strip(value)


class NoteUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=100)
    content: str | None = Field(default=None, min_length=1, max_length=5000)
    category: str | None = Field(default=None, min_length=1, max_length=50)
    pinned: bool | None = None

    @field_validator("title", "content", "category", mode="before")
    @classmethod
    def strip_text(cls, value):
        return _strip(value)

    @field_validator("title", "content", "pinned")
    @classmethod
    def required_fields_cannot_be_null(cls, value):
        if value is None:
            raise ValueError("cannot be null; leave the field out to keep it")
        return value


class NoteOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    content: str
    category: str | None = None
    pinned: bool
    created_at: datetime
    updated_at: datetime
