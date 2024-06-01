from asap.engine.pets import Pet


class InvalidActionError(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return f"Invalid Action: {self.message}"


class TeamFullError(InvalidActionError):
    def __init__(self):
        super().__init__(message="Team is full.")


class NotEnoughMoneyError(InvalidActionError):
    def __init__(self, money: int, price: int):
        super().__init__(message=f"Price {price} too expensive for money {money}.")


class PositionOccupiedError(InvalidActionError):
    def __init__(self, i: int):
        super().__init__(message=f"Position {i} already occupied.")


class AlreadyBoughtError(InvalidActionError):
    def __init__(self, pet: Pet):
        super().__init__(message=f"Pet {pet} already bought.")
