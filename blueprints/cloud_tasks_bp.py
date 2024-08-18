from flask import Blueprint, request, jsonify
from service.gcloud_storage_service import GcloudStorageService
from service.surgeon_crawler import SurgeonCrawler
from service.firestore_service import FirestoreService
from service.gcloud_tasks_service import GcloudTasksService
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
        GcloudTasksService.create_zipcode_task(first_zip_code, 1)
        return "success"
    except Exception:
        logging.error(traceback.format_exc())
        return "error", 500


@cloud_tasks_bp.route("/continue_crawl/dfc2d27b2dbb4417926d8e396737a76a", methods=["POST"])
def continue_crawl():
    """When the Gcloud http tasks get run they will run this api function passing in a zipcode
    Creates a new http task after the zipcode is done being crawled with the next zipcode in the dataset
    @return:
    """
    try:
        zipcode_json = request.get_json()
        current_zipcode = zipcode_json["zipcode"]
        print(f"Fetching surgeons: {current_zipcode}")
        crawler = SurgeonCrawler(current_zipcode)

        try:
            surgeon_data = crawler.crawl_surgeons()
        except:
            surgeon_data = []

        for surgeon in surgeon_data:
            if FirestoreService.surgeon_exists(surgeon):
                print(f"Surgeon exists: {surgeon['name_text']}. Continue...")
            else:
                print(f"Surgeon does not exists: {surgeon['name_text']}. Inserting...")
                FirestoreService.insert_surgeon(surgeon)

        next_zipcode = GcloudStorageService.get_next_zipcode(current_zipcode)
        if next_zipcode:
            GcloudTasksService.create_zipcode_task(next_zipcode, 1)
        return "success"
    except Exception:
        logging.error(traceback.format_exc())
        return "success"
