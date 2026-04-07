"""imports or reads your raw dataset; if you scraped, include scraper here"""

import json
from google_play_scraper import app, Sort, reviews

#scrape reviews, limit at 3000 reviews. Last name = F, so app = wysa
result, _ = reviews(
    "bot.touchkin",
    lang='en',
    country='ca',
    sort=Sort.NEWEST, #most recent reviews
    count=3000
)

#save into JSONL file and seperate with newline, utf-8 maintains original text
with open("../data/reviews_raw.jsonl", "w", encoding="utf-8") as f:
    for review in result:
        f.write(json.dumps(review, default=str) + "\n")
