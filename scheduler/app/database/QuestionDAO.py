import pymongo
from datetime import datetime
from StudentDAO import StudentDAO
class QuestionDAO(object):
    def __init__(self, database):
        self.collection = database.question
        self.studentDao = StudentDAO(database)
    
    def getNextQuestionId(self):
        return (self.collection.count() + 1)

    def addQuestion(self, user_id, question, answer=None):
        newId = self.getNextQuestionId()
        if isinstance(user_id, basestring):
            student = self.studentDao.findStudentByUsername(user_id)
            user_id = student['userid']
        q = {'id': int(newId), "user_id": user_id, 'question': question, 'answer': answer, 'timestamp': datetime.now()}
        self.collection.insert_one(q)

    def getQuestions(self):
        return self.collection.find({}).sort('timestamp', pymongo.DESCENDING)

    def answerQuestion(self, question_id, answer):
        self.collection.update({"id": int(question_id)}, {"$set": {'answer': answer, 'timestamp' : datetime.now()}})

    def getUnansweredQuestions(self):
        return self.collection.find({'answer': None}).sort('timestamp', pymongo.DESCENDING)

    def getAnsweredQuestions(self):
        return self.collection.find({'answer': {'$ne': None}}).sort('timestamp', pymongo.DESCENDING)

    def getQuestionsByStudent(self, user_id):
        if isinstance(user_id, basestring):
            student = self.studentDao.findStudentByUsername(user_id)
            user_id = student['userid']
        return self.collection.find({'user_id' : user_id}).sort('timestamp', pymongo.DESCENDING)

    def getQuestionById(self, question_id):
        return self.collection.find_one({'id': int(question_id)})
