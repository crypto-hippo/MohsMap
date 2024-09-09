from flask import Blueprint, request, jsonify
from service.gcloud_storage_service import GcloudStorageService
from service.surgeon_crawler import SurgeonCrawler
from service.firestore_service import FirestoreService
from service.gcloud_tasks_service import GcloudTasksService
import traceback
import logging
import json


surgeon_bp = Blueprint('surgeon_bp', __name__, url_prefix='/surgeon')


@surgeon_bp.route("/warmup", methods=["GET"])
def warmup():
    return "Hot!"


@surgeon_bp.route("/get", methods=["GET"])
def get_surgeons():
    try:
        return jsonify(
            FirestoreService.get_all_surgeons()
        )
    except:
        return jsonify([])


@surgeon_bp.route("/search", methods=["POST"])
def surgeon_search():
    """
    @return:
    """

    print("searching surgeons")
    try:
        search_data = request.get_json()
        search_value: str = search_data.get("search_value")
        search_value = search_value.strip()
        if len(search_value) == 5 and search_value.isdigit():
            result = FirestoreService.search_by_zip(search_value)
        else:
            result = FirestoreService.search_by_name_or_city(search_value)

    except Exception:
        print(traceback.format_exc())
        result = {"error": "Unable to process request"}

    return jsonify(result)
