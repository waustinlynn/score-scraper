from typing import List

from pydantic import BaseModel


class TeamScore(BaseModel):
    team_name: str
    score: int
    home: bool

class GameScore(BaseModel):
    game_id: int
    team_scores: List[TeamScore]

class SportScores(BaseModel):
    sport: str
    state: str
    scores: List[GameScore]