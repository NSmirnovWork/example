from model import User


class UsersService:
    def get_users(self, page, page_size):
        # simulate API
        total = 123

        items = [
            User(id=i, name=f"User {i}", email=f"user{i}@gmail.com")
            for i in range((page - 1) * page_size, page * page_size)
        ]

        return type("Result", (), {"items": items, "total": total})()
