from typing import Annotated

from pydantic import BaseModel, StringConstraints


class StatusResponse(BaseModel):
    status: str


class UserResponse(BaseModel):
    name: str
    email: str


class PetCreate(BaseModel):
    id: int
    name: str
    species: str
    age: int


class UserCreate(BaseModel):
    login: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    name: Annotated[str, StringConstraints(min_length=6, max_length=20)]
    email: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    password: Annotated[str, StringConstraints(min_length=6, max_length=32)]