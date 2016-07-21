from datetime import datetime
import pymongo
from StudentDAO import StudentDAO

class RecommendationDAO(object):
    
    def __init__(self, db):
        self.collection = db.course_recommendations   
        self.studentDao = StudentDAO(db)
    
    #recommendedCourses is intended as a LIST of course ids
    #course_input is optional and only used in Shadow case. It is a list showing the capacities of the courses, in order. This is essentially the replacement
    #for the gurobi input on course capacity in the shadow mode case.
    def addRecommendationHistory(self, user_id_recommendation, semesterId, recommendedCourses, is_shadow=False , user_id_run_by=None , course_input = None):
        
        #If user_id_run is not provided, assume the student is running it for himself.
        if user_id_run_by is None: user_id_run_by = user_id_recommendation
        data={'user_id_recommendation': user_id_recommendation, 
              'user_id_run_by':user_id_run_by,
              'recommendedCourses' : recommendedCourses, 
              'semester' : semesterId, 
              'timestamp' : datetime.now(),
              'is_shadow' : is_shadow, 
              'course_input' : course_input}
        
        self.collection.insert_one(data)
        
    #Return recommendation cursor from newest to olders
    def findRecommendationsForStudentById(self,userId, show_shadow=False):
        print 'in recommendationDAO.findRecommendationsById', userId
        results = []
        cursor = self.collection.find({'user_id_recommendation' : userId, 'is_shadow' : show_shadow}).sort('timestamp', pymongo.DESCENDING)
        for document in cursor:
            results.extend(document['recommendedCourses'])
        return results
#         return self.collection.find({'user_id_recommendation' : userId, 'is_shadow' : show_shadow}).sort('timestamp', pymongo.DESCENDING)

    def findRecommendationsForStudentByUsername(self, username,show_shadow=False):
        print 'in recommendationDAO.findRecommendationsByUsername', username
        student = self.studentDao.findStudentByUsername(username)
        print 'in recommendationDAO.findRecommendationsByUsername', student
        if student != None:
            return self.findRecommendationsForStudentById(student['userid'],show_shadow)
        else:
            return None

    def findAllStudentRecommendations(self, show_shadow=False):
        recommendation_dictionary = {}
        students = self.studentDao.find_all_students()

        for student in students:
            recommendation_dictionary[student['userid']] = self.findRecommendationsForStudentById(student['userid'],show_shadow)

        return recommendation_dictionary
    
    def clearOutExistingRecommendations(self):
        self.collection.remove({})