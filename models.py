from pydantic import BaseModel


class NoteMetadata(BaseModel):
    title: str
    tags: list[str]
    sentiment: str
    key_entities: list[str]

