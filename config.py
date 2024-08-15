import os

config = {
    "secret_key": "04d87dfb6f9846a499d7ddb4dec1fca8",
}

blueprints_dir = os.path.join(
    os.getcwd(),
    "blueprints"
)

project_id = "mohsmap"
zip_code_tasks_queue = "zip-code-tasks"
gcloud_region = "us-central1"

service_account_path = os.path.join(
    os.getcwd(),
    "mohsmap-5688f444cd0a.json"
)
