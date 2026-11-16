from fastapi import HTTPException, status

from project.models import Pet, User, UserRole
from project.repositories import (
    DuplicatePetError,
    DuplicateUserError,
    PetRepository,
    UserRepository,
)
from project.schemas import PetCreate, UserCreate


class UserService:
    def __init__(self, user_repository: UserRepository) -> None:
        self.__user_repository = user_repository

    async def signup(self, user: UserCreate) -> User:
        role = (
            UserRole.ADMIN
            if not await self.__user_repository.has_users()
            else UserRole.USER
        )
        model = User(
            id=0,
            login=user.login,
            name=user.name,
            email=user.email,
            password=user.password,
            role=role,
        )
        try:
            return await self.__user_repository.save(model)
        except DuplicateUserError as error:
            label = "логином" if error.field == "login" else "почтой"
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Пользователь с таким {label} уже существует",
            ) from error

    async def get_by_id(self, user_id: int) -> User:
        user = await self.__user_repository.get_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
        return user

    async def get_by_login(self, login: str) -> User:
        user = await self.__user_repository.get_by_login(login)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден",
            )
        return user

    async def get_all(self) -> list[User]:
        return await self.__user_repository.get_all()


class PetService:
    def __init__(self, pet_repository: PetRepository) -> None:
        self.__pet_repository = pet_repository

    async def create(self, pet: PetCreate) -> Pet:
        model = Pet(**pet.model_dump())
        try:
            return await self.__pet_repository.save(model)
        except DuplicatePetError as error:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Животное с таким id уже существует",
            ) from error

    async def get_by_id(self, pet_id: int) -> Pet:
        pet = await self.__pet_repository.get_by_id(pet_id)
        if pet is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Животное не найдено",
            )
        return pet

    async def get_all(self) -> list[Pet]:
        return await self.__pet_repository.get_all()
