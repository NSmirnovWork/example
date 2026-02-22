class UserUpdate:
    def __init__(self, id: int, name: str | None, email: str | None):
        self.id = id
        self.name = name
        self.email = email
