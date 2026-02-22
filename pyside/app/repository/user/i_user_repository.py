from abc import ABC

from ...domain.user.user import User

from ...core.pagination import PaginationRequest, PaginationResponse
from ...domain.user.user_create import UserCreate
from ...domain.user.user_update import UserUpdate


class IUserRepository(ABC):
    async def list(
        self, pagination_request: PaginationRequest
    ) -> PaginationResponse[User]:
        raise NotImplementedError

    async def create(self, user_create: UserCreate) -> int:
        raise NotImplementedError

    async def get(self, id: int) -> User | None:
        raise NotImplementedError

    async def update(self, user_update: UserUpdate) -> bool:
        raise NotImplementedError

    async def delete(self, id: int) -> bool:
        raise NotImplementedError
