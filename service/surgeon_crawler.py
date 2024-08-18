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
            soup.select_one(".cardInfo.alert").text.split(" ")[-1]
        )

    @classmethod
    def get_soup(cls, url):
        page_content = requests.get(url).content
        soup = BeautifulSoup(page_content, "html.parser")
        return soup

    @classmethod
    def parse_phone(cls, location_row):
        last_address_div = location_row.select(".address div")[-1]
        phone_text = last_address_div.text
        num_digits = 0
        for possible_digit in phone_text:
            if possible_digit.isdigit():
                num_digits += 1
        if num_digits >= 10:
            return phone_text
        return ""

    @classmethod
    def parse_lat_lng(cls, location_row):
        lat_lng_link: Tag = location_row.select_one(".directions a")
        href = lat_lng_link["href"]
        lat_lng = href[href.rindex("/")+1:]
        lat, lng = lat_lng.split(",")
        return lat, lng

    @classmethod
    def get_name(cls, card: Tag):
        name = card.select_one(".card-header").select_one('.providername').text
        name = name.replace(",", "")
        return name.split(" "), name

    @classmethod
    def parse_location_divs(cls, location_row):
        divs = location_row.select(".address div")
        return [div.text for div in divs]

    @classmethod
    def atleast_5_digits(cls, text):
        num_digits = 0
        for letter_index in range(len(text)):
            letter = text[letter_index]
            if letter.isdigit():
                num_digits += 1
        return num_digits >= 5

    @classmethod
    def parse_city_state_zip(cls, location_row):
        city, state, zipcode = None, None, None
        address_elements: list[Tag] = location_row.select(".address div")
        # print(f"Num address elements: {len(address_elements)}")
        for div in address_elements:
            if "," in div.text:
                args = div.text.split(", ")
                if len(args) == 2 and len(args[1].split(" ")) == 2:
                    city = args[0]
                    state, zipcode = args[1].split(" ")

        return city, state, zipcode

    def create_url(self) -> str:
        url = f"https://www.mohscollege.org/find-a-surgeon/index.php?City=&State=&ZipCode={self.zipcode}&Distance=100&Country=&LastName=&Search=Search&page={str(self.page)}#directoryresultstop"
        print(f"Fetching surgeons from url: {url}")
        return url

    def parse_surgeons(self, soup):
        surgeon_data = []
        surgeon_cards: list[Tag] = soup.select(".card.cardInfo")
        for card in surgeon_cards:
            name_tokens, name_text = self.get_name(card)
            # print(f"Name: {name}")
            rows: list[Tag] = card.select(".row")
            # print(f"Num rows: {len(rows)}")
            for row in rows:
                location_divs = self.parse_location_divs(row)
                city, state, zipcode = self.parse_city_state_zip(row)
                if not (city and state and zipcode):
                    print(f"Could not parse city, state, zipcode for location under: {name_text}")

                if zipcode and len(zipcode) == 4:
                    zipcode = f"0{zipcode}"

                phone = self.parse_phone(row)
                lat, lng = self.parse_lat_lng(row)

                new_surgeon = {
                    "name_tokens": name_tokens,
                    "name_text": name_text,
                    "location_divs": location_divs,
                    "location_text": "-".join(location_divs),
                    "city": city.lower() if city else "",
                    "state": state.lower() if state else "",
                    "zipcode": zipcode,
                    "phone": phone,
                    "lat": lat,
                    "lng": lng
                }

                surgeon_data.append(new_surgeon)

        return surgeon_data

    @classmethod
    def log_objects(cls, objs: list):
        print("\n")
        for surgeon in objs:
            for k, v in surgeon.items():
                print(f"{k}: {v}")
            # input(">>>: Any key for next surgeon")
            print("\n")

    def crawl_surgeons(self):
        url = self.create_url()
        soup = self.get_soup(url)
        num_pages = self.get_num_pages(soup)

        all_surgeons = []

        print("Page: 1")
        first_page_surgeons = self.parse_surgeons(soup)

        # self.log_objects(first_page_surgeons)

        all_surgeons.extend(first_page_surgeons)

        if num_pages > 1:
            page_range = range(2, num_pages + 1)
            for p in page_range:
                time.sleep(5)
                print(f"Page: {p}")
                self.page = p
                url = self.create_url()
                soup = None
                while True:
                    try:
                        soup = self.get_soup(url)
                        break
                    except:
                        print("Error while fetching soup: retrying...")
                        time.sleep(5)

                next_surgeons = self.parse_surgeons(soup)

                # self.log_objects(next_surgeons)

                all_surgeons.extend(next_surgeons)

        return all_surgeons

"""
db schema 

{
    "provider_name": "provider_name",
}
"""

# if __name__ == "__main__":
#     surgeon_crawler = SurgeonCrawler("00501")
#     surgeons = surgeon_crawler.crawl_surgeons()
#     surgeon_crawler.log_objects(surgeons)
