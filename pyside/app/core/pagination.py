from dataclasses import dataclass


@dataclass
class PaginationRequest:
    page: int
    per_page: int


@dataclass
class PaginationResponse[T]:
    page: int
    per_page: int
    total: int | None
    items: list[T]
