import pandas as pd


def obtain_players_from_lineup(lineup: dict, dx_team) -> list:
    team = lineup["response"][dx_team]
    startXI = [players["player"]["name"] for players in team["startXI"]]
    substit = [players["player"]["name"] for players in team["substitutes"]]
    return [*startXI, *substit]


def obtain_played_minutes_from_lineup(lineup: dict, events: dict, dx_team: int, team: str) -> list:
    player_minutes = _setup_player_minutes(lineup, dx_team)
    who_out = obtain_info_out(events, team)
    who_in = obtain_info_in(events, team)
    for player in list(who_out.keys()):
        player_minutes.loc[player_minutes.player == player, "minutes"] = who_out[player]
    for player in list(who_in.keys()):
        player_minutes.loc[player_minutes.player == player, "minutes"] = who_in[player]
    return player_minutes


def _setup_player_minutes(lineup, dx_team):
    team = lineup["response"][dx_team]
    players = obtain_players_from_lineup(lineup, dx_team)
    minutes = [*[90 for _ in team["startXI"]], *[0 for _ in team["substitutes"]]]
    player_minutes = pd.DataFrame(list(zip(players, minutes)), columns=["player", "minutes"])
    return player_minutes


def obtain_info_in(events: dict, team: str) -> dict:
    in_p = obtain_getin(events, team)
    minutes = [90 - minute for minute in obtain_time_of_substitution(events, team)]
    return dict(zip(in_p, minutes))


def obtain_info_out(events: dict, team: str) -> dict:
    in_p = obtain_who_getout(events, team)
    minutes = obtain_time_of_substitution(events, team)
    return dict(zip(in_p, minutes))


def obtain_getin(events: dict, team: str) -> list:
    return _obtain_substitutes(events, in_or_out="assist", team=team)


def obtain_who_getout(events: dict, team: str) -> list:
    return _obtain_substitutes(events, in_or_out="player", team=team)


def obtain_time_of_substitution(events: dict, team: str) -> list:
    ins = [
        event["time"]["elapsed"]
        for event in events["response"]
        if ((event["type"] == "subst") & (event["team"]["name"] == team))
    ]
    return ins


def _obtain_substitutes(events: dict, in_or_out: str, team: str) -> list:
    ins = [
        event[in_or_out]["name"]
        for event in events["response"]
        if ((event["type"] == "subst") & (event["team"]["name"] == team))
    ]
    return ins
