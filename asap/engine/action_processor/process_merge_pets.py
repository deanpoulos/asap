from asap.actions import ActionMergePets

from asap.engine.action_processor._errors import InvalidMergeError
from asap.engine.action_processor.merge_pets import merge_pets
from asap.team import Team


def process_merge_pets(action: ActionMergePets, team: Team, game):
    from asap.engine.game import Game
    game: Game
    if (
        # both positions must exist
        (action.position_from not in team.pets or
         action.position_to not in team.pets) or
        # both positions must be occupied
        (team.pets[action.position_from] is None or
         team.pets[action.position_to] is None) or
        # both must be the same pet type
        (not isinstance(team.pets[action.position_from],
                        type(team.pets[action.position_to]))) or
        # neither must be maximum level
        (team.pets[action.position_from].level == game.settings.max_pet_level or
         team.pets[action.position_to].level == game.settings.max_pet_level)
    ):
        raise InvalidMergeError(action.position_from, action.position_to)

    # combine pets
    giving_pet = team.pets[action.position_from]
    receiving_pet = team.pets[action.position_to]

    team.remove_pet(action.position_from)

    merge_pets(giving_pet, receiving_pet, game.team_states[team])


