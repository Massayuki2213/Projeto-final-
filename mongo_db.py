import pymongo
from pymongo import MongoClient

class MongoDB:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['agenda_telefonica']
        self.collection = self.db['contatos']

    def get_next_id(self):
        # Recupera o maior ID e incrementa em 1
        last_contact = self.collection.find_one(sort=[("id", pymongo.DESCENDING)])
        if last_contact:
            return last_contact['id'] + 1
        else:
            return 1

    def insert(self, name, number):
        # Adicionar um ID único
        contact_id = self.get_next_id()
        contact = {"id": contact_id, "name": name, "number": number}
        self.collection.insert_one(contact)

    def search_by_id(self, contact_id):
        return self.collection.find_one({"id": contact_id})

    def search_by_name(self, name):
        return list(self.collection.find({"name": {"$regex": f".*{name}.*", "$options": "i"}}))

    def search_suggestions(self, prefix):
        return list(self.collection.find({"name": {"$regex": f"^{prefix}", "$options": "i"}}, {"id": 1, "name": 1}))

    def delete_by_id(self, contact_id):
        self.collection.delete_one({"id": contact_id})

    def delete_by_name(self, name):
        self.collection.delete_many({"name": {"$regex": f"^{name}$", "$options": "i"}})

    def list_contacts(self):
        return list(self.collection.find())
