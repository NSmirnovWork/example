from ...core.pagination import PaginationRequest, PaginationResponse
from ...domain.user.user import User
from ...domain.user.user_create import UserCreate
from ...domain.user.user_update import UserUpdate
from .i_user_repository import IUserRepository


class FakeUserRepository(IUserRepository):
    def __init__(self):
        self._users: list[User] = [
            User(i, f"Test {i}", f"test{i}@gmail.com") for i in range(1, 12)
        ]

    async def list(
        self, pagination_request: PaginationRequest
    ) -> PaginationResponse[User]:
        from_ = (pagination_request.page - 1) * pagination_request.per_page
        to_ = (pagination_request.page) * pagination_request.per_page
        return PaginationResponse(
            page=pagination_request.page,
            per_page=pagination_request.per_page,
            total=len(self._users),
            items=self._users[from_:to_],
        )

    async def create(self, user_create: UserCreate) -> int:
        user = User(
            self._users[-1].id + 1 if self._users else 1,
            user_create.name,
            user_create.email,
        )
        self._users.append(user)
        return user.id

    async def get(self, id: int) -> User | None:
        for user in self._users:
            if user.id == id:
                return user
        return None

    async def update(self, user_update: UserUpdate) -> bool:
        for user in self._users:
            if user.id == user_update.id:
                user.name = user_update.name or user.name
                user.email = user_update.email or user.email
                return True
        return False

    async def delete(self, id: int) -> bool:
        for user in self._users:
            if user.id == id:
                self._users.remove(user)
                return True
        return False
