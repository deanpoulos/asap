from asap.foods import Food


class BreadCrumbs(Food):
    base_attack = 1
    base_health = 0

    def __init__(self, attack: int = base_attack, health: int = base_health):
        self._attack = attack
        self._health = health
        self._perk = None
