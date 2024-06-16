from asap.pets import Pet
from asap.team import TeamShopState


def merge_pets(giving_pet: Pet, receiving_pet: Pet, state: TeamShopState):
    """ leaves `giving_pet` unchanged, merged pet is modified `receiving_pet`. """

    # combine stats by taking max of each from both pet
    receiving_pet.extra_health = max(giving_pet.extra_health, receiving_pet.extra_health)
    receiving_pet.extra_attack = max(giving_pet.extra_attack, receiving_pet.extra_attack)

    # combine exp
    receiving_pet.add_exp(giving_pet.exp + 1, state)
