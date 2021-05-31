"""
Author: Dinesh Sadhwani
Email: dsadhwa1@binghamton.edu

A Python script to scrape all games data from api.rawg.op

This script uses the scrapy package and extends the scrapy.Spider class to build
a spider that can scrape websites and APIs. In this particular script, we use the Spider class to scrape the API provided by https://rawg.io to get data of 500,000+ video games

"""

# -*- coding: utf-8 -*-
import scrapy
import json
from dotenv import load_dotenv
import os

# load environment variable to get API key
load_dotenv()

RAWG_API_KEY = os.environ.get("RAWG_API_KEY")


class GamesSpider(scrapy.Spider):
    name = "games"
    allowed_domains = ["api.rawg.io"]

    # start_urls indicates the url from where the spider will start crawling
    start_urls = [
        f"https://api.rawg.io/api/games?key={RAWG_API_KEY}&page_size=40"]

    def parse(self, response):
        # deserialize json response and convert to python dictionary
        # we face an encoding issue here which is solved by setting
        # FEED_EXPORT_ENCODING = 'utf-8' in ../settings.py
        response = json.loads(response.body)
        results = response["results"]

        # interating over the list of results to extract relevant data
        for result in results:
            # some games do not have an esrb rating. Hence, the check
            if result["esrb_rating"]:
                esrb_rating = result["esrb_rating"]["name"]
            else:
                esrb_rating = None

            yield {
                "id": result["id"],
                "name": result["name"],
                "release_date": result["released"],
                "avg_rating": result["rating"],
                # using list comprehension to get a list of list containing
                # the type of rating ("exceptional", "meh", etc) and its count
                "ratings_dist": [{"title": rating["title"], "count": rating["count"]} for rating in result["ratings"]],
                "no_of_ratings": result["ratings_count"],
                "metacritic_score": result["metacritic"],
                # create a list of genres
                "genres": [genre["name"] for genre in result["genres"]],
                # create a list of tags assigned by players
                "tags": [tag["name"] for tag in result["tags"]],
                "esrb_rating": esrb_rating
            }

        # check if next page exists. If it does, then scrape it too
        next_page = response["next"]

        if next_page:
            yield scrapy.Request(
                url=next_page,
                callback=self.parse
            )
