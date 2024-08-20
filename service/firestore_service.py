from google.cloud import firestore
from google.cloud.firestore_v1 import DocumentSnapshot, FieldFilter


class FirestoreService:

    client = firestore.Client(database='mohsmap')
    surgeons = client.collection("surgeons")

    @classmethod
    def surgeon_exists(cls, surgeon):
        """Surgeon exists if the name, and the location elements match an existing record
        """
        name_text = surgeon["name_text"]
        location_text = surgeon["location_text"]
        existing_surgeon_query = (cls.surgeons
                                  .where(filter=FieldFilter("name_text", "==", name_text))
                                  .where(filter=FieldFilter("location_text", "==", location_text)))
        results = list(existing_surgeon_query.stream())
        print(f"Surgeon exists: {results}")
        return len(results) > 0

    @classmethod
    def insert_surgeon(cls, surgeon):
        cls.surgeons.add(surgeon)

    @classmethod
    def get_all_surgeons(cls):
        surgeons = cls.surgeons.stream()
        surgeons = [
            {"document_id": s.id, **s.to_dict()} for s in surgeons
        ]
        return surgeons

    @classmethod
    def serialize_documents(cls, result_set):
        return list(map(lambda r: {"document_id": r.id, **r.to_dict()}, result_set))

    @classmethod
    def search_by_zip(cls, search_value):
        result = cls.surgeons.where(filter=FieldFilter("zipcode", "==", search_value)).stream()
        return cls.serialize_documents(result)

    @classmethod
    def search_by_name(cls, search_value: str):
        if " " in search_value:
            search_value = search_value.split(" ")
        else:
            search_value = [search_value]

        for i in range(len(search_value)):
            search_value[i] = search_value[i].capitalize()

        print("search value", search_value)
        result = list(cls.surgeons.where(filter=FieldFilter("name_tokens", "array_contains_any", search_value)).stream())
        args = cls.serialize_documents(result)
        return args

    @classmethod
    def search_by_city(cls, search_value):
        search_value = search_value.lower()
        result = cls.surgeons.where(filter=FieldFilter("city", "==", search_value)).stream()
        return cls.serialize_documents(result)

    @classmethod
    def search_by_name_or_city(cls, search_value):
        by_name = cls.search_by_name(f"{search_value}")
        by_city = cls.search_by_city(search_value)
        by_name.extend(by_city)
        return by_name

