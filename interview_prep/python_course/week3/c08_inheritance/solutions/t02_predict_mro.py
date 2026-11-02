class Base:
    def setup(self):
        return ["Base"]


class Logged(Base):
    def setup(self):
        return ["Logged"] + super().setup()


class Authorized(Base):
    def setup(self):
        return ["Authorized"] + super().setup()


class Retrying(Authorized):
    def setup(self):
        return ["Retrying"] + super().setup()


class Final(Logged, Retrying):
    def setup(self):
        return ["Final"] + super().setup()


ANSWER_MRO = ["Final", "Logged", "Retrying", "Authorized", "Base", "object"]
ANSWER_CALLS = ["Final", "Logged", "Retrying", "Authorized", "Base"]
