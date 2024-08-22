from google.cloud.storage import Client
from google.cloud.storage.bucket import Bucket


class GcloudStorageService:

    storage_bucket_name = "mohsmap.appspot.com"
    zipcodes_file_name = "zip_codes.txt"

    @classmethod
    def download_zip_codes(cls):
        storage_client = Client()
        bucket: Bucket = storage_client.bucket(cls.storage_bucket_name)
        blob = bucket.blob(cls.zipcodes_file_name)
        contents = blob.download_as_text()
        zipcodes = contents.split("\n")
        zipcodes = list(filter(lambda x: len(x), zipcodes))
        return zipcodes

    @classmethod
    def get_first_zip_code(cls):
        zipcodes = cls.download_zip_codes()
        return zipcodes[0]

    @classmethod
    def get_next_zipcode(cls, current_zipcode, num_ahead):

        result = None
        zipcodes = cls.download_zip_codes()
        if zipcodes[-1] == current_zipcode:
            print("Last zipcode crawled. Chillin")
        else:
            current_index = zipcodes.index(current_zipcode)
            try:
                result = zipcodes[current_index + num_ahead]
            except:
                pass
        return result

    @classmethod
    def get_last_zipcode(cls):
        zipcodes = cls.download_zip_codes()
        return zipcodes[-1]

    @classmethod
    def get_previous_zipcode(cls, zipcode):
        zipcodes = cls.download_zip_codes()
        index = zipcodes.index(zipcode)
        if index == 0:
            return None
        else:
            return zipcodes[index-1]


