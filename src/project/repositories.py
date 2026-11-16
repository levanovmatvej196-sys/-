from project.models import Pet, User


class DuplicateUserError(Exception):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"User {field} already exists")


class DuplicatePetError(Exception):
    pass


class UserRepository:
    def __init__(self) -> None:
        self.__last_id = 0
        self.__users_by_id: dict[int, User] = {}
        self.__user_ids_by_login: dict[str, int] = {}
        self.__user_ids_by_email: dict[str, int] = {}

    async def save(self, user: User) -> User:
        login_key = user.login.strip().casefold()
        email_key = user.email.strip().casefold()

        if login_key in self.__user_ids_by_login:
            raise DuplicateUserError("login")
        if email_key in self.__user_ids_by_email:
            raise DuplicateUserError("email")

        self.__last_id += 1
        user.id = self.__last_id
        self.__users_by_id[self.__last_id] = user
        self.__user_ids_by_login[login_key] = self.__last_id
        self.__user_ids_by_email[email_key] = self.__last_id
        return user

    async def get_by_id(self, user_id: int) -> User | None:
        return self.__users_by_id.get(user_id)

    async def get_by_login(self, login: str) -> User | None:
        user_id = self.__user_ids_by_login.get(login.strip().casefold())
        return self.__users_by_id.get(user_id) if user_id is not None else None

    async def has_users(self) -> bool:
        return bool(self.__users_by_id)

    async def get_all(self) -> list[User]:
        return list(self.__users_by_id.values())


class PetRepository:
    def __init__(self) -> None:
        self.__pets_by_id: dict[int, Pet] = {}

    async def save(self, pet: Pet) -> Pet:
        if pet.id in self.__pets_by_id:
            raise DuplicatePetError(f"Pet {pet.id} already exists")
        self.__pets_by_id[pet.id] = pet
        return pet

    async def get_by_id(self, pet_id: int) -> Pet | None:
        return self.__pets_by_id.get(pet_id)

    async def get_all(self) -> list[Pet]:
        return list(self.__pets_by_id.values())