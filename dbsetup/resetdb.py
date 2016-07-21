#
# Usage: python resetdb.py 'database name'
#
import pymongo
from sys import argv as args

db_name=args[1]
conn = pymongo.MongoClient()
conn.drop_database(db_name)
