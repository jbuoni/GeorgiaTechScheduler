#
# General accessor/modifier for Teaching Assistants and Professors
#
import pymongo

class FacultyDAO(object):
    #Static members -- DO NOT CHANGE WHILE USING
    TA_ONLY = 0
    PROF_ONLY = 1

    def __init__(self, database):
        self.ta_collection = database.ta
        self.prof_collection = database.professor

    def findAllTAs(self):
        return self.ta_collection.find().sort('userid', pymongo.ASCENDING)

    def findAllProfessors(self):
        return self.prof_collection.find().sort('userid', pymongo.ASCENDING)

    def findFacultyForCourseSemester(self, searchType, courseid, semesterid):

        if searchType == FacultyDAO.TA_ONLY:
            return self.ta_collection.find({'course_semester' : {'$elemMatch' : {'$eq' : [courseid, semesterid] } } }).sort(pymongo.ASCENDING)

        elif searchType == FacultyDAO.PROF_ONLY:
            return self.prof_collection.find({'course_semester' : {'$elemMatch' : {'$eq' : [courseid, semesterid] } } }).sort(pymongo.ASCENDING)
        
        else:
            #TODO: Eventually provide a way of returning TAs and Professors together
            print "Invalid Selection Chosen!"
            return None
