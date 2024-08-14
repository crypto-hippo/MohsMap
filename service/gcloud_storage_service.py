from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket


class GcloudStorageService:

    storage_bucket_name = "mohsmap.appspot.com"
    zipcodes_file_name = "zip_codes.txt"

    @classmethod
    def get_first_zip_code(cls):
        storage_client = Client()
        bucket: Bucket = storage_client.bucket(cls.storage_bucket_name)
        blob = bucket.blob(cls.zipcodes_file_name)
        contents = blob.download_as_text()
        zipcodes = contents.split("\n")
        zipcodes = list(filter(lambda x: len(x), zipcodes))
        return zipcodes[0]

