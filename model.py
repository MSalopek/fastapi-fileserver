from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel

class SearchResponse(BaseModel):
    files: list[str]

class RenameRequest(BaseModel):
    from_name: str
    to_name: str

