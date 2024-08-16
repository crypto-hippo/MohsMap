from bs4 import BeautifulSoup, Tag
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import time
import requests 
import json 
import logging 
import traceback


class SurgeonCrawler:

    def __init__(self, zipcode):
        self.zipcode = zipcode
        self.page = 1

    @classmethod
    def get_num_pages(cls, soup):
        return int(
            soup.select(".cardInfo.alert").text[-2:]
        )

    @classmethod
    def get_soup(cls, url):
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content)
        return soup

    @classmethod
    def parse_phone(cls, last_address_div):
        phone_text = last_address_div.text
        num_digits = 0
        for possible_digit in phone_text:
            if possible_digit.isdigit():
                num_digits += 1
        if num_digits >= 10:
            return phone_text
        return ""

    @classmethod
    def parse_address_phone(cls, card):
        address: Tag = card.select(".card-body").select_one(".address")
        address_divs: list[Tag] = address.select('div')
        phone = cls.parse_phone(address_divs[-1])
        if phone:
            del address_divs[-1]
        address_args = [addr.text for addr in address_divs]
        return address_args, phone

    @classmethod
    def parse_lat_lng(cls, card):
        pass

    @classmethod
    def get_name(cls, card: Tag) -> str:
        return card.select(".card-header").select('.providername').text

    def create_url(self) -> str:
        return f"https://www.mohscollege.org/find-a-surgeon/index.php?City=&State=&ZipCode={self.zipcode}&Distance=200&Country=&LastName=&Search=Search&page={str(self.page)}#directoryresultstop"

    def parse_surgeons(self, soup):
        surgeons = []
        surgeon_cards: list[Tag] = soup.select(".card.cardInfo")
        for card in surgeon_cards:
            name: str = self.get_name(card)
            address, phone = self.parse_address_phone(card)
            lat, lng = self.parse_lat_lng(card)
        return []

    def crawl_surgeons(self):
        url = self.create_url()
        soup = self.get_soup(url)
        num_pages = self.get_num_pages(soup)

        all_surgeons = []

        first_page_surgeons = self.parse_surgeons(soup)
        all_surgeons.extend(first_page_surgeons)

        if num_pages > 1:
            page_range = range(2, num_pages + 1)
            for p in page_range:
                self.page = p
                url = self.create_url()
                soup = self.get_soup(url)
                next_surgeons = self.parse_surgeons(soup)
                all_surgeons.extend(next_surgeons)

"""
db schema 

{
    "provider_name": "provider_name",
    
}
"""
