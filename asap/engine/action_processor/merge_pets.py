from asap.pets import Pet


def merge_pets(giving_pet: Pet, receiving_pet: Pet):
    """ leaves `giving_pet` unchanged, merged pet is modified `receiving_pet`. """

    # combine stats by taking max of each from both pet
    receiving_pet.extra_health = max(giving_pet.extra_health, receiving_pet.extra_health)
    receiving_pet.extra_attack = max(giving_pet.extra_attack, receiving_pet.extra_attack)

    # combine exp
    for _ in range(giving_pet.exp + 1):
        if receiving_pet.exp == 5:
            continue
        receiving_pet.add_1_exp()
