#
# Basic DAO accessor/modifier for course collection. 
# All methods, unless otherwise noted will return the result of a query that the user will have to traverse
#


import pymongo

class CourseDAO(object):
    def __init__(self, database):
        self.collection = database.course
        self.concentrations = database.concentrations

    def findCoursesForSemester(self, semesterId):
        return self.collection.find({"semesters":{ "$elemMatch" : {"$eq":semesterId}}} ).sort('courseid', pymongo.ASCENDING)

    def findAllCourses(self):
        return self.collection.find().sort('courseid', pymongo.ASCENDING)

    def findCourseById(self, courseId):
        return self.collection.find_one({'courseid': courseId})
    
    def findAllConcentrations(self):
        return self.concentrations.find().sort('id',pymongo.ASCENDING)
    
    def findConcentrationById(self, concentrationId):
        return self.concentrations.find_one({'id' : concentrationId})
    
    def setCourseCapacity(self, courseId, newCapacity):
        self.collection.update({'courseid': courseId}, {"$set": {'capacity': newCapacity}})
     
    def setCourseFallTerm(self, courseId, offered):
        self.collection.update({'courseid': courseId}, {"$set": {'fallterm': offered}})

    def setCourseSpringTerm(self, courseId, offered):
        self.collection.update({'courseid': courseId}, {"$set": {'springterm': offered}})

    def setCourseSummerTerm(self, courseId, offered):
        self.collection.update({'courseid': courseId}, {"$set": {'summerterm': offered}})

    def setCourseAvaiability(self, courseId, availability):
        self.collection.update({'courseid': courseId}, {"$set": {'availability': availability}})

    def setCourseTAPool(self, courseId, newTAPool):
        # self.collection.update({'courseid': courseId}, {"$set": {'ta': newTAPool}})
        pass

    def addSemesterAvailable(self,courseId, semesterId):
        course = self.findCourseById(courseId)
        course['semesters'].append(semesterId)
        self.collection.update({'courseid':courseId}, {"$set" : {'semesters' : course['semesters']}})
        
    
    def removeSemesterAvailable(self,courseId, semesterId):
        course = self.findCourseById(courseId)
        course['semesters'].remove(semesterId)
        self.collection.update({'courseid':courseId}, {"$set" : {'semesters' : course['semesters']}})

    

