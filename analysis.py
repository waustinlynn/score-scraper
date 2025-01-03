from typing import List

from models import SportScores
from score import GameScore

def flatten(game: GameScore, sport: str, state: str) -> dict:
    return {
        "game_id": game.game_id,
        "team_name": game.team_scores[0].team_name,
        "score": f"{game.team_scores[0].score}-{game.team_scores[1].score}",
        "opponent": game.team_scores[1].team_name,
        "sport": sport,
        "state": state
    }

def flatten_results(sport_scores_data: List[SportScores]) -> List[dict]:
    game_scores = []
    for sport_data in sport_scores_data:
        game_scores.extend([flatten(game, sport_data.sport, sport_data.state) for game in sport_data.scores])
            
    return game_scores

def calculate_score_differential(score: str) -> int:
    """
    Score will be in the format "team-opponent"
    """
    team_score, opponent_score = score.split("-")
    return int(team_score) - int(opponent_score)