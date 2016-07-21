#
# General Accessor/Modifier for Semester Collection
#


import pymongo

class SemesterDAO(object):
    def __init__(self, database):
        self.collection=database.semester

    def findAllSemesters(self):
        return self.collection.find().sort('semester', pymongo.ASCENDING)

    def findSemester(self, semesterid):
        return self.collection.find_one({'semester' : semesterid})


