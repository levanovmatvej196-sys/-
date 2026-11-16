from enum import StrEnum

from pydantic import BaseModel


class UserRole(StrEnum):
    ADMIN = "ADMIN"
    USER = "USER"

class User(BaseModel):
    id: int
    login: str
    name: str
    email: str
    password: str
    role: UserRole


class Pet(BaseModel):
    id: int
    name: str
    species: str
    age: int
