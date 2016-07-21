import pymongo
from datetime import datetime
class ConcentrationDAO(object):
    def __init__(self, database):
        self.collection = database.concentration

    def get_concentration(self, concentration_id):
        return self.collection.find_one({'id': concentration_id})

    def get_concentration_name(self, concentration_id):
        return self.collection.find_one({'id': concentration_id})['name']
