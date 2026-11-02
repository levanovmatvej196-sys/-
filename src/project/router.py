# Обрабатываем соединение 
from fastapi import APIRouter,status , HTTPException

from project.schemas import StatusResponse,UserResponse, User,  Pet
router =APIRouter()

users_database=dict[str,User]()
pets_database: dict[int, Pet] = {}

@router.get("/status")
def get_status()-> StatusResponse:
    return StatusResponse(status='ok')


@router.get("/status")
def get_email()-> UserResponse:
    return UserResponse(email='Levkhh')

@router.post("/signup")
def signup(user:User):
    global users_database
    if user.login in users_database:
        raise HTTPException(409)
    users_database[user.login]=user

@router.get("/users/{login}")
def get_user(login: str)->UserResponse:
    if login not in users_database:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    user=users_database[login]
    return UserResponse(
        name=user.name,
        email=user.email,
        )

@router.post("/pets", status_code=status.HTTP_201_CREATED)
def create_pet(pet: Pet) -> Pet:
    if pet.id in pets_database:
        raise HTTPException(status.HTTP_409_CONFLICT, "Животное с таким id уже существует")
    pets_database[pet.id] = pet
    return pet

@router.get("/pets/{pet_id}")
def get_pet(pet_id: int) -> Pet:
    if pet_id not in pets_database:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Животное не найдено")
    return pets_database[pet_id]


# Доп. задание
@router.get("/pets")
def get_all_pets() -> list[Pet]:
    return list(pets_database.values())