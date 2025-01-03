from typing import List
from bs4 import BeautifulSoup

from models import GameScore, TeamScore


class ScoreParser:
    def parse_html(self, html_content: str) -> List[GameScore]:
        soup = BeautifulSoup(html_content, "html.parser")
        game_divs = soup.find_all("div", class_="gameContainer")
        games: List[GameScore] = []
        for game_div in game_divs:
            games.append(self.parse_score(game_div))
        return games

    def parse_score(self, game_div) -> GameScore:

        game_id = game_div.find('a', {'data-gameid': True})['data-gameid']

        team_score_divs = game_div.find_all('div', class_='teamScore')
        team_scores: List[TeamScore] = []

        for team_score in team_score_divs:
            team_name = team_score.find('div', class_='name').text.strip()
            
            score = team_score.find('div', class_='score').text.strip()
            home = True            

            if 'away' in team_score.find('div', class_='score')['class']:
                home = False
                
            team_scores.append(TeamScore(**{"team_name": team_name, "score": score, "home": home}))

        return GameScore(**{"game_id": game_id, "team_scores": team_scores})
