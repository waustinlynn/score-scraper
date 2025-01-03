## High School Sport Score Scraper

This scraper uses python to pull high school sport scores by state and sport and display the resulting data in pandas data frames.

### Installation
Ensure a recent installation of python (3.11 was used for this example)

```
python -m venv .venv
<activate virtual environment based on OS>
pip install -r requirements.txt
playwright install
python main.py
```

### Approach

Data Used:

```
sports = [
    "football",
    "girls-basketball",
    "boys-basketball",
    "lacrosse",
    "hockey"
]

states = [
    "georgia",
    "virginia",
    "california",
    "texas",
    "florida",
    "new-york",
    "north-carolina",
    "south-carolina",
    "alabama",
    "tennessee"
]
```

The script will combine each sport with the state and call scorestream.com with the appropriate path parameters using asyncio for asynchronous querying of each web page.
The results will then be aggregated into an array of objects that will then be flattened and provided to a pandas DataFrame.

Note: each call has a 60 second timeout and some calls will fail intermittently.

The results will then be output to the console - exact logic can be found in `main.py`

### Considerations
The scope of scoring is limited to just a few sports that have a clean winner score and loser score. Sports with different scoring (such as tennis) are out of scope for this example. 

The scraping uses the `playwright` library. This was chosen due to it's ability to handle web page loading including content rendered by javascript. The base web pages do not include the scores as they are called via ajax request and loaded dynamically. The line `await page.wait_for_selector("div#exploreScores", timeout=60000)` in `html_parser.py` will wait until the appropriate div is rendered on the page before considering the page loading complete. 

In a production scenario, it would be advised to emit each combination of state and sport in an event and have the consumer of the event handle the call to the web page. 
This would offer the following benefits:
  * Can reject the event and retry with exponential backoff in the event of a timeout or other transient failure.
  * Can control the consumption of the events to not overload the source.

Another drawback is that it appears to only fetch 50 scores at most (as suggested by the API payload below). This can be seen in the "Game Counts by State and Sport" DataFrame. It wasn't immediately obvious how this could be increased (or if pagination was available), but exploring the API option outlined below is a possible path forward. 

#### API

There is an actual api call to fetch the data with what appears to be appropriate payload parameters:

```
{
    "method": "games.search",
    "params": {
        "isExploreSearch": true,
        "aboveConfidenceGrade": 30,
        "afterDateTime": "2024-12-26 14:14:12",
        "beforeDateTime": "2025-01-03 14:14:12",
        "location": {
            "country": "US",
            "city": "Cumming",
            "latitude": 34.1483,
            "longitude": -84.1404,
            "state": "GA"
        },
        "sportNames": [
            "football"
        ],
        "squadIds": [
            1010,
            1020,
            1030
        ],
        "country": "US",
        "state": "GA",
        "offset": 0,
        "count": 50,
        "apiKey": "a20bd983-0147-437a-ab6d-49afeb883d33"
    }
}
```
However, if calling the api directly without the appropriate cookie header, the payload sent appears to be ignored and some default data (college football scores) is returned. More investigation would be needed to see if this could be reverse engineered to use the api exclusively rather than web page scraping.  

There also exists a [blog post](https://blog.scorestream.com/scorestream-local-sports-api/) that indicates an official API to access scorestream data, however it requires an commercial partnership. If this partnership is possible, this would be a better alternative as the solution required would be more robust and officially supported by scorestream. 