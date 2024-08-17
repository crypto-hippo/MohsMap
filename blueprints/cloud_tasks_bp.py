from flask import Blueprint, request, jsonify
from service.gcloud_storage_service import GcloudStorageService
from service.surgeon_crawler import SurgeonCrawler
from service.firestore_service import FirestoreService
import traceback
import logging

cloud_tasks_bp = Blueprint('cloud_tasks_bp', __name__, url_prefix='/cloud_tasks')


@cloud_tasks_bp.route("/start_crawl/e86fc4d3b30d4f4f947f13c0a128377d")
def start_crawl():
    """This function is called by the app engine cron job to start the crawl loop. See cron.yaml
    All this function does is create the initial gcloud http task with the first zipcode
    @return:
    """
    try:
        logging.info("[+] Fetching zip_codes.txt from Google Cloud Storage")
        first_zip_code = GcloudStorageService.get_first_zip_code()
        logging.info(f"[+] Creating gcloud http task with first zipcode: {first_zip_code}")
        return "success"
    except Exception:
        logging.error(traceback.format_exc())
        return "error", 500


@cloud_tasks_bp.route("/continue_crawl/dfc2d27b2dbb4417926d8e396737a76a")
def continue_crawl():
    """When the Gcloud http tasks get run they will run this api function passing in a zipcode
    Creates a new http task after the zipcode is done being crawled with the next zipcode in the dataset
    @return:
    """
    try:
        zipcode_json = request.get_json()
        next_zipcode = zipcode_json["zipcode"]
        crawler = SurgeonCrawler(next_zipcode)
        surgeon_data = crawler.crawl_surgeons()
        for surgeon in surgeon_data:
            if FirestoreService.surgeon_exists(surgeon):
                print(f"Surgeon exists: {surgeon["name_text"]}. Continue...")
            else:
                print(f"Surgeon does not exists: {surgeon["name_text"]}. Inserting...")
        
    except Exception:
        logging.error(traceback.format_exc())
