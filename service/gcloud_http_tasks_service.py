from google.cloud import tasks_v2
from config import project_id, gcloud_region, zip_code_tasks_queue
from service.datetime_service import DatetimeService
from google.api_core.exceptions import AlreadyExists
import uuid
import logging
import json
import traceback


class GcloudTasksService:
    tasks_client = tasks_v2.CloudTasksClient()

    @classmethod
    def get_tasks_parent(cls, queue_name):
        return cls.tasks_client.queue_path(project_id, gcloud_region, queue_name)

    @classmethod
    def create_zipcode_task(cls, zipcode: str):
        """Accepts zipcode and the index of the zipcode within the zip_codes.txt inside gcloud storage
        Will use the zipcode as the task_id
        @param zipcode:
        @return:
        """
        task_id = zipcode
        new_task = tasks_v2.Task()
        new_task.http_request = tasks_v2.HttpRequest()
        new_task.http_request.http_method = tasks_v2.HttpMethod.POST
        new_task.http_request.url = "https://mohsmap.uc.r.appspot.com/cloud_tasks/continue_crawl/dfc2d27b2dbb4417926d8e396737a76a"
        new_task.http_request.headers = {"content-type": "application/json"}
        new_task.http_request.body = json.dumps({"zipcode": zipcode}).encode()
        new_task.name = cls.tasks_client.task_path(project_id, gcloud_region, zip_code_tasks_queue, task_id)
        task_request = tasks_v2.CreateTaskRequest()
        task_request.parent = cls.get_tasks_parent(zip_code_tasks_queue)
        task_request.task = new_task
        cls.tasks_client.create_task(task_request)
