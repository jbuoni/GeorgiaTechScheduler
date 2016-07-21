from pymongo import MongoClient
from bson.json_util import dumps
from sys import argv as args

db_name=args[1]


client = MongoClient()

db = client[db_name]

students = db.student

cursor = students.find()

print 'PRINTING STUDENTS!\n'
for entry in cursor:
    print dumps(entry, indent=4, sort_keys=True)


print '\n\nPRINTING PROFESSORS!\n'
cursor = db.professor.find()
for entry in cursor:
    print dumps(entry, indent=4, sort_keys=True)

courses = db.course

cursor = courses.find()

print '\n\nPRINTING COURSES!\n'
for entry in cursor:
    print dumps(entry, indent=4, sort_keys=True)

concentrations = db.concentrations
for entry in  concentrations.find():
    print dumps(entry, indent=4, sort_keys=True)
