from asap.engine.pets import Pet


def sell_price_pet(pet: Pet, base_price: int) -> int:
    return base_price * pet.level
