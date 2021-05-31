"""
Author: Dinesh Sadhwani
Email: dsadhwa1@binghamton.edu

A Python script to scrape all game publishers data from api.rawg.op

This script uses the scrapy package and extends the scrapy.Spider class to build
a spider that can scrape websites and APIs. In this particular script, we use the Spider class to scrape the API provided by https://rawg.io to get data of 47,000+ game publishers

"""

import scrapy
import json
from dotenv import load_dotenv
import os

load_dotenv()

RAWG_API_KEY = os.environ.get("RAWG_API_KEY")


class PublishersSpider(scrapy.Spider):
    name = "publishers"
    allowed_domains = ["api.rawg.io"]
    start_urls = [
        f"https://api.rawg.io/api/publishers?key={RAWG_API_KEY}&page_size=40"]

    def parse(self, response):
        # deserialize json response and convert to python dictionary
        # we face an encoding issue here which is solved by setting
        # FEED_EXPORT_ENCODING = 'utf-8' in ../settings.py
        response = json.loads(response.body)
        results = response["results"]

        for result in results:
            yield {
                "pub_id": result["id"],
                "pub_name": result["name"],
                "games": [game["id"] for game in result["games"]]
            }

        next_page = response["next"]

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )
