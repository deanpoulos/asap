from typing import Type

import pytest

from asap.engine.engine.game import Game
from asap.engine.engine.game_settings import GameSettings
from asap.engine.foods import Apple
from asap.engine.pets import Duck, Pet
from asap.engine.shop.settings import SettingsPetShop, SettingsFoodShop


@pytest.fixture()
def game_turn_1_2_teams():
    settings_pet_shop = SettingsPetShop(TIER_2_PETS=[Duck])
    settings_food_shop = SettingsFoodShop(TIER_1_FOODS=[Apple])

    game_settings = GameSettings(
        num_teams=2,
        settings_pet_shop=settings_pet_shop,
        settings_food_shop=settings_food_shop,
        starting_turn=1
    )
    return Game(settings=game_settings)


@pytest.fixture()
def game_turn_1_ducks_only_apples_only_single_team():
    settings_pet_shop = SettingsPetShop(TIER_1_PETS=[Duck])
    settings_food_shop = SettingsFoodShop(TIER_1_FOODS=[Apple])

    game_settings = GameSettings(
        num_teams=1,
        settings_pet_shop=settings_pet_shop,
        settings_food_shop=settings_food_shop,
        starting_turn=1
    )
    return Game(settings=game_settings)


@pytest.fixture()
def game_turn_1_ducks_only_apples_only_single_team_with_tier2_dummy(DummyTier2Pet):
    settings_pet_shop = SettingsPetShop(TIER_1_PETS=[Duck], TIER_2_PETS=[DummyTier2Pet])
    settings_food_shop = SettingsFoodShop(TIER_1_FOODS=[Apple])

    game_settings = GameSettings(
        num_teams=1,
        settings_pet_shop=settings_pet_shop,
        settings_food_shop=settings_food_shop,
        starting_turn=1
    )
    return Game(settings=game_settings)


@pytest.fixture()
def DummyTier2Pet() -> Type[Pet]:
    class Dummy(Duck):
        pass

    return Dummy
