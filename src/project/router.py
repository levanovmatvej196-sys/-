from typing import Annotated

from fastapi import APIRouter, Depends, Request, status

from project.models import Pet
from project.schemas import PetCreate, StatusResponse, UserCreate, UserResponse
from project.services import PetService, UserService

router = APIRouter()


def get_user_service(request: Request) -> UserService:
    return request.app.state.user_service


def get_pet_service(request: Request) -> PetService:
    return request.app.state.pet_service


UserServiceDep = Annotated[UserService, Depends(get_user_service)]
PetServiceDep = Annotated[PetService, Depends(get_pet_service)]


@router.get("/status", response_model=StatusResponse)
def get_status() -> StatusResponse:
    return StatusResponse(status="ok")


@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, user_service: UserServiceDep) -> UserResponse:
    created_user = await user_service.signup(user)
    return UserResponse(name=created_user.name, email=created_user.email)


@router.get("/users/{login}", response_model=UserResponse)
async def get_user(login: str, user_service: UserServiceDep) -> UserResponse:
    user = await user_service.get_by_login(login)
    return UserResponse(name=user.name, email=user.email)


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(user_service: UserServiceDep) -> list[UserResponse]:
    users = await user_service.get_all()
    return [UserResponse(name=user.name, email=user.email) for user in users]


@router.post("/pets", status_code=status.HTTP_201_CREATED, response_model=Pet)
async def create_pet(pet: PetCreate, pet_service: PetServiceDep) -> Pet:
    return await pet_service.create(pet)


@router.get("/pets/{pet_id}", response_model=Pet)
async def get_pet(pet_id: int, pet_service: PetServiceDep) -> Pet:
    return await pet_service.get_by_id(pet_id)


@router.get("/pets", response_model=list[Pet])
async def get_all_pets(pet_service: PetServiceDep) -> list[Pet]:
    return await pet_service.get_all()
