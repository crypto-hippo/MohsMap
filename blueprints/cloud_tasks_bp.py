import traceback
from flask import Blueprint, request, jsonify
import logging

cloud_tasks_bp = Blueprint('cloud_tasks_bp', __name__, url_prefix='/cloud_tasks')


@cloud_tasks_bp.route("/start_crawl/e86fc4d3b30d4f4f947f13c0a128377d")
def start_crawl():
    """This function is called by the app engine cron job to start the crawl loop. See cron.yaml
    All this function does is create the initial gcloud http task with the first zipcode
    @return:
    """
    try:
        task_json = request.get_json()
        zipcode = task_json.get("next_zip_code")
        if zipcode:
            logging.info(f"Checking for new surgeons under zip: {zipcode}")
        else:
            logging.info(f"No zipcode found: starting with the first one")
    except Exception:
        logging.error(traceback.format_exc())


@cloud_tasks_bp.route("/continue_crawl")
def continue_crawl():
    try:
        pass
    except Exception:
        print(traceback.format_exc())