from asap.shop.item import Item


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


class PositionNotOccupiedError(InvalidActionError):
    def __init__(self, i: int):
        super().__init__(message=f"There is no pet in position {i}.")


class AlreadyUnfrozenError(InvalidActionError):
    def __init__(self, item: Item):
        super().__init__(message=f"Item {item} is already unfrozen.")


class AlreadyFrozenError(InvalidActionError):
    def __init__(self, item: Item):
        super().__init__(message=f"Item {item} is already frozen.")


class AlreadyBoughtError(InvalidActionError):
    def __init__(self, shop_index: int):
        super().__init__(message=f"Item {shop_index} already bought.")


class InvalidSwapError(InvalidActionError):
    def __init__(self, pet_position_1: int, pet_position_2: int):
        super().__init__(message=f"Invalid swap {pet_position_1} to {pet_position_2}")


class InvalidMergeError(InvalidActionError):
    def __init__(self, pet_position_1: int, pet_position_2: int):
        super().__init__(message=f"Invalid merge from team position {pet_position_1} to {pet_position_2}")


class InvalidBuyMergeError(InvalidActionError):
    def __init__(self, shop_index: int, pet_position: int):
        super().__init__(message=f"Invalid merge from shop position {shop_index} "
                                 f"to team position {pet_position}")
