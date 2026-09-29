from pydantic import BaseModel


class SaveNoteArgs(BaseModel):
    content: str
    tags: list[str]


class SearchNotesArgs(BaseModel):
    query: str