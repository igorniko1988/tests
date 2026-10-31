class Session:
    created = 0
    active = 0

    def __init__(self) -> None:
        Session.created += 1
        Session.active += 1
        self.number = Session.created
        self.closed = False

    def close(self) -> None:
        if not self.closed:
            self.closed = True
            Session.active -= 1

    @classmethod
    def reset_counters(cls) -> None:
        cls.created = 0
        cls.active = 0
