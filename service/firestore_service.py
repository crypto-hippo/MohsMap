from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter


class FirestoreService:

    client = firestore.Client()

    @classmethod
    def surgeon_exists(cls, surgeon):
        """Surgeon exists if the name, and the location elements match an existing record
        """
        name_text = surgeon["name_text"]
        location_text = surgeon["location_text"]
        existing_surgeon_query = (cls.client.collection("surgeons")
                                  .where(filter=FieldFilter("name_text", "==", name_text))
                                  .where(filter=FieldFilter("location_text", "==", location_text)))
        results = list(existing_surgeon_query.stream())
        print(f"Surgeon exists: {results}")


