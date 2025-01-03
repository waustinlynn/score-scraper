from typing import List


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

def get_combined_data() -> List[dict]:
    data = []
    for state in states:
        for sport in sports:
            data.append({"state": state, "sport": sport})
    return data