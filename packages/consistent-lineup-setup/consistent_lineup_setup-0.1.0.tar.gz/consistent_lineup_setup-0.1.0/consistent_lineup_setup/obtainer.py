from consistent_lineup_setup import obtain_played_minutes_from_lineup


class Obtainer_Played_Minutes:
    def __init__(self) -> None:
        self._events = None
        self._lineup = None
        self.played_minutes = None
        self.dx_team = None
        self.team = None

    def set_events(self, events) -> None:
        self._events = events

    def set_lineup(self, lineup) -> None:
        self._lineup = lineup

    def obtain_played_minutes(self, dx_team: int = 0) -> None:
        self.dx_team = dx_team
        self.team = self._lineup["response"][self.dx_team]["team"]["name"]
        self.played_minutes = obtain_played_minutes_from_lineup(
            self._lineup, self._events, self.dx_team, self.team
        )
        self.played_minutes["team"] = self.team
