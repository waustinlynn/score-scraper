import asyncio
from typing import List
from models import SportScores
from playwright.async_api import async_playwright
from score import ScoreParser

class PlaywrightParser():

    def __init__(self):
        self.score_parser = ScoreParser()

    async def parse_page(self, browser, sport: dict) -> SportScores:
        page = await browser.new_page()
        try:
            url = f"https://scorestream.com/explore/r/{sport['state']}/high-school/{sport['sport']}/scores"
            print(f"Scraping {url}")
            await page.goto(url, timeout=60000)
            await page.wait_for_selector("div#exploreScores", timeout=60000)
            content = await page.content()
            print(f"Completed {url}")
            return SportScores(**{"sport": sport['sport'], "state": sport['state'], "scores":  self.score_parser.parse_html(content)})
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return None
        finally:
            await page.close()

    async def parse(self, sport_data: List[dict]) -> List[SportScores]:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            tasks = []
            for sport in sport_data:
                task = self.parse_page(browser, sport)
                tasks.append(task)
            results = await asyncio.gather(*tasks)
            return [result for result in results if result is not None]
