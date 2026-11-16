from fastapi import FastAPI

from project.router import router
from project.repositories import PetRepository, UserRepository
from project.services import PetService, UserService

app = FastAPI()
app.state.user_service = UserService(UserRepository())
app.state.pet_service = PetService(PetRepository())

app.include_router(router)
