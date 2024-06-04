# mongo_db.py

from pymongo import MongoClient

class MongoDB:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="agenda", collection_name="contatos"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def insert(self, name, number):
        contact = {"name": name, "number": number}
        self.collection.insert_one(contact)

    def search(self, name):
        contact = self.collection.find_one({"name": {"$regex": f"^{name}$", "$options": "i"}})
        if contact:
            return contact["number"]
        return None

    def delete(self, name):
        self.collection.delete_one({"name": {"$regex": f"^{name}$", "$options": "i"}})

    def list_contacts(self):
        contacts = self.collection.find()
        return [(contact["name"], contact["number"]) for contact in contacts]
