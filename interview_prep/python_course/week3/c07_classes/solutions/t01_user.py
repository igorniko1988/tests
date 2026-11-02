class User:
    def __init__(self, name: str, email: str) -> None:
        name = name.strip()
        if not name:
            raise ValueError("name must not be empty")
        self.name = name
        self.email = email  # через setter — валидация в одном месте

    @property
    def email(self) -> str:
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        value = value.strip().lower()
        local, at, domain = value.partition("@")
        if not at or not local or "@" in domain or "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise ValueError(f"invalid email: {value!r}")
        self._email = value

    @property
    def domain(self) -> str:
        return self._email.split("@")[1]
