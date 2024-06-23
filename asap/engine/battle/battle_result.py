from asap.team.team import Team


class TeamBattleResult:
    class Result:
        WIN = 0
        DRAW = 1
        LOSS = 2

    def __init__(self, result: Result, team: Team):
        self.result = result
        self.team = team


class BattleResult:
    def __init__(self, team_l_result: TeamBattleResult, team_r_result: TeamBattleResult):
        self.team_l_result = team_l_result
        self.team_r_result = team_r_result

    def __iter__(self):
        yield self.team_l_result
        yield self.team_r_result


WIN = TeamBattleResult.Result.WIN
DRAW = TeamBattleResult.Result.DRAW
LOSS = TeamBattleResult.Result.LOSS
