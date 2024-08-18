from flask import Blueprint, request, jsonify
from service.gcloud_storage_service import GcloudStorageService
from service.surgeon_crawler import SurgeonCrawler
from service.firestore_service import FirestoreService
from service.gcloud_tasks_service import GcloudTasksService
import traceback
import logging

surgeon_bp = Blueprint('surgeon_bp', __name__, url_prefix='/surgeon')


@surgeon_bp.route("/get", methods=["GET"])
def get_surgeons():
    try:
        return jsonify(
            FirestoreService.get_all_surgeons()
        )
    except:
        return jsonify([])
