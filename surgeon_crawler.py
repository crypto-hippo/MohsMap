from bs4 import BeautifulSoup, Tag
from google.cloud import storage
from google.cloud.storage.bucket import Bucket
import time
import requests 
import json 
import logging 
import traceback

storage_bucket_name = "mohsmap.appspot.com"
zipcodes_file_name = "zip_codes.txt"


def download_zip_codes():
    storage_client = storage.Client()
    bucket: Bucket = storage_client.bucket(storage_bucket_name)
    blob = bucket.blob(zipcodes_file_name)
    contents = blob.download_as_text()
    zipcodes = contents.split("\n")
    zipcodes = list(filter(lambda x: len(x), zipcodes))
    return zipcodes


def create_url(zipcode: str, page: int) -> str:
    return f"https://www.mohscollege.org/find-a-surgeon/index.php?City=&State=&ZipCode={zipcode}&Distance=200&Country=&LastName=&Search=Search&page={str(page)}#directoryresultstop"


def crawl_by_zip(zip: str):
    zipcodes = download_zip_codes()




# from urllib3 import PoolManager
# from urllib3.contrib.appengine import AppEngineManager, is_appengine_sandbox

# if is_appengine_sandbox():
#     # AppEngineManager uses AppEngine's URLFetch API behind the scenes
#     http = AppEngineManager()
# else:
#     # PoolManager uses a socket-level API behind the scenes
#     http = PoolManager()

# class SurgeonCrawler(object):
#
#     def __init__(self, zipcodes):
#         self.root_url = "https://www.mohscollege.org"
#         self.surgeon_finder_root_url = "https://www.mohscollege.org/surgeon-finder/"
#         self.zipcodes = zipcodes
#         self.headers = {
#             "User-Agent": "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"
#         }
#
#
#     def parse_lat_lng(self, markup):
#         links = markup.find_all("a")
#         lat_lng_link = filter(lambda link: link.get_text() == "Get Directions", links)[0]
#         href = lat_lng_link["href"]
#         lat_lng_start_index = href.rfind("/") + 1
#         lat_lng = href[lat_lng_start_index:]
#         return lat_lng
#
#     def format_address(self, location_markup):
#         location = str(location_markup).split("</legend>")[1]
#         location = location.split("</fieldset>")[0]
#         elements = location.split("<br/>")
#         location_csv = "|".join(elements)
#         return location_csv
#
#     def parse_locations(self, location_markup):
#         locations = []
#         for location in location_markup:
#             current_location = {}
#             current_location["location_title"] = location.select("legend")[0].get_text()
#             current_location["address"] = self.format_address(location)
#             locations.append(current_location)
#         return json.dumps(locations)
#
#     def parse_phone_detail(self, headers, directory_str):
#         for header in headers:
#             if header.get_text() == "Phone":
#                 header_str = str(header)
#                 header_str_index = directory_str.index(header_str)
#                 content = directory_str[header_str_index + len(header_str):]
#                 phone = content[0:content.index("<")]
#                 return phone
#
#         return ''
#
#     def format_languages(self, languages):
#         return "||".join(languages)
#
#     def parse_languages(self, headers, directory_str, languages):
#         for header in headers:
#             if header.get_text() == "Languages":
#                 header_str = str(header)
#                 header_str_index = directory_str.index(header_str)
#                 content = directory_str[header_str_index + len(header_str):]
#                 next_langle_index = content.index("<")
#                 ending_html_1 = "<br/><br/>"
#                 ending_html_2 = "<h3>"
#
#                 if ending_html_1 in content:
#                     done_index_1 = content.index(ending_html_1)
#                     if done_index_1 == next_langle_index:
#                         language = content[0:done_index_1]
#                         languages.append(language)
#                         return self.format_languages(languages)
#
#                 if ending_html_2 in content:
#                     done_index_2 = content.index(ending_html_2)
#                     if done_index_2 == next_langle_index:
#                         language = content[0:done_index_2]
#                         languages.append(language)
#                         return self.format_languages(languages)
#
#                 elif content[next_langle_index: next_langle_index + 5] == "<br/>":
#                     return self.parse_languages("<br/>", content, languages)
#         return ''
#
#     def parse_details(self, parser):
#         details = {}
#         directory_str = str(parser.select("#directory")[0])
#         directory = parser.select("#directory")[0]
#
#         detail_headers = directory.findChildren("h3", recursive=False)
#         # for header in detail_headers:
#
#         details["phone"] = self.parse_phone_detail(detail_headers, directory_str)
#
#         details["languages"] = self.parse_languages(detail_headers, directory_str, [])
#         details["training"] = self.parse_training(detail_headers, directory)
#
#         return details
#
#     def parse_training(self, headers, directory):
#         for header in headers:
#             if header.get_text() == "Training":
#                 directory_string = str(directory)
#                 training_index = directory_string.index(str(header))
#                 training_paragraphs = []
#                 all_paragraphs = directory.select("p")
#
#                 for p in all_paragraphs:
#                     p_str = str(p)
#                     p_str_index = directory_string.index(p_str)
#                     if p_str_index > training_index:
#                         args_split = p_str.split("<br/>")
#                         args_joined = "|".join(args_split)
#                         soup = BeautifulSoup(args_joined, "html.parser")
#                         training_paragraphs.append(soup.get_text())
#
#                 return "||".join(training_paragraphs)
#
#         return ''
#
#     def add_details_to_surgeon(self, markup, session, surgeon):
#         detail_link = markup.select(".detailLink a")[0]
#
#         if detail_link:
#             detail_page_url = self.surgeon_finder_root_url + detail_link["href"]
#             detail_markup = session.get(detail_page_url, headers=self.headers).content
#             detail_parser = BeautifulSoup(detail_markup, "html.parser")
#             locations = detail_parser.select("#directory fieldset")
#
#             surgeon["locations"] = self.parse_locations(locations)
#             details = self.parse_details(detail_parser)
#
#             for key in details:
#                 surgeon[key] = details[key]
#
#         return surgeon
#
#     def create_surgeon(self, markup, session):
#         surgeon = {}
#         surgeon["title"] = markup.select(".providername")[0].get_text()
#         surgeon["latlng"] = self.parse_lat_lng(markup)
#         surgeon = self.add_details_to_surgeon(markup, session, surgeon)
#         return surgeon
#
#     def crawl_pages(self, current_zip, session, current_page, surgeons):
#         try:
#             logging.info("Fetching page: %s" % current_page)
#             time.sleep(3)
#
#             content = session.get(current_page, headers=self.headers).content
#             parser = BeautifulSoup(content, 'html.parser')
#             next_surgeon_markup = parser.find_all("div", class_="providerContainer")
#
#             for surgeon in next_surgeon_markup:
#                 next_surgeon = self.create_surgeon(surgeon, session)
#                 surgeons.append(next_surgeon)
#
#             links = parser.find_all("a")
#             for link in links:
#                 if link.get_text() == "Next":
#                     return self.crawl_pages(current_zip, session, self.root_url + str(link["href"]) , surgeons)
#
#             return surgeons
#
#         except Exception as e:
#             logging.info(str(e))
#             return surgeons
#
#     def crawl(self):
#         try:
#             session = requests.Session()
#             submit_disclaimer_form = session.post("https://www.mohscollege.org/surgeon-finder/disclaimer.php?mode=disclaimer", data={"agree": "yes"}, headers=self.headers)
#             initial_page = "https://www.mohscollege.org/surgeon-finder/index.php?City=&State=&ZipCode=%s&Distance=200&Country=&LastName=&Search=Search#directoryresultstop"
#
#             all_surgeons = []
#
#             for code in self.zipcodes:
#                 next_surgeons_found = self.crawl_pages(code, session, initial_page % code, [])
#                 all_surgeons.extend(next_surgeons_found)
#
#             # for surgeon in all_surgeons:
#             #     for key in surgeon:
#             #         logging.info(key)
#             #         logging.info(surgeon[key])
#             return all_surgeons
#
#         except Exception as e:
#             logging.info(str(e))
#             return []
        #     all_surgeons.extend(next_surgeons_found)

        # return jsonify(format_surgeons(all_surgeons))
