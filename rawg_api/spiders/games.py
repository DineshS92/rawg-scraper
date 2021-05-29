import scrapy
import json
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.environ.get("RAWG_API_KEY")


class GamesSpider(scrapy.Spider):
    name = "games"
    allowed_domains = ["api.rawg.io"]
    start_urls = [
        f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size=40"]

    def parse(self, response):
        # return json.loads(response.body)
        pass
