from asap.engine.actions import ActionMergePets


def validate_merge_pets(action: ActionMergePets, team_shop_state, max_pet_level: int) -> bool:
    team = team_shop_state.team
    return not (
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
        (team.pets[action.position_from].level == max_pet_level or
         team.pets[action.position_to].level == max_pet_level)
    )
