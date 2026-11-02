# Формат тела ответа 
from pydantic import BaseModel


class StatusResponse(BaseModel):
    status: str

class UserResponse(BaseModel):
    email: str


class User(BaseModel):
    login: str
    name: str
    email: str
    password: str

class Pet(BaseModel):
    id: int
    name: str
    species: str   # вид: кошка, собака...
    age: int
