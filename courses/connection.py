import pymongo

class Connection:
    def __init__(self):
        self.connect_string = "mongodb://localhost:27017"
        self.mongo_client = pymongo.MongoClient(self.connect_string)
        self.dbname = self.mongo_client['LMS']
        self.collection = ""
    def set_collection(self, collection_name):
        self.collection = self.dbname[collection_name]
        return self.collection