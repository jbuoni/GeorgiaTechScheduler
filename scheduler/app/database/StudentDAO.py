#
# Standard Student collection accessor/modifier
#

import pymongo

class StudentDAO(object):

    def __init__(self, database):
        self.collection = database.student

    def findStudentById(self,studentId):
        return self.collection.find_one({'userid' : studentId})
    
    def findStudentByUsername(self,username):
        print 'in StudentDAO.findStudentByUsername', username
        return self.collection.find_one({'username' : username})

    def findAllStudents(self):
        return self.collection.find().sort('userid', pymongo.ASCENDING)
    
    def setUserConcentrationById(self,userId, concentrationId):
        self.collection.update({"userid":userId},{"$set":{'concentration':concentrationId}})
     
    def setUserConcentrationByUsername(self,username, concentrationId):
        self.collection.update({"username":username},{"$set":{'concentration':concentrationId}})
     
    def setPreferredCoursesById(self, userId, semesterId, courses):
        doc = self.findStudentById(userId)
        preferred = doc['requestedcourses']
        preferred[str(semesterId)]=courses
        self.collection.update({'userid':userId}, {"$set":{'requestedcourses':preferred}})
        
    def setPreferredCoursesByUsername(self,username,semesterId,courses):
        doc = self.findStudentByUsername(username)
        preferred = doc['requestedcourses']
        preferred[str(semesterId)]=courses
        self.collection.update({'username':username}, {"$set":{'requestedcourses':preferred}})
        
    def setGPAByUsername(self,username,gpa):
        self.collection.update({'username' : username},{"$set":{'gpa':gpa}})
        
    def setCreditsEarnedByUsername(self,username,credits_earned):
        self.collection.update({'username' : username},{"$set":{'credits_earned':credits_earned}})
        
    def completeCourseByUsername(self,username,courseId,numCredits):
        doc =self.findStudentByUsername(username)
        temp = doc['completed']
        temp.append(courseId)
        doc['completed']=temp
        doc['credits_earned'] = doc['credits_earned'] + numCredits
        self.collection.update({'username': username}, doc)
        
    def setGraduationByUsername(self,username, graduation):
        self.collection.update({'username': username},{"$set":{'graduation':graduation}})
    
    def setCoursesCompletedByUsername(self,username,completed):
        self.collection.update({'username': username}, {"$set":{'completed': completed}})
        
    def addCompletedCourse(self, username, courseId):
        completed = self.findStudentByUsername(username)['completed']
        completed.append(courseId)
        self.setCoursesCompletedByUsername(username, completed)
        
        
    def findInterest(self,courseId,semesterId):
        
        return self.collection.count({'requestedcourses': [semesterId, courseId]})
