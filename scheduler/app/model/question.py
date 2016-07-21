from ..model import questionDao


def question_list():
    questions = questionDao.getQuestions()
    question_ids = []
    for question in questions:
        question_ids.append(question[''])
    return question_ids

def unanswered_question_list():
    questions = questionDao.getUnansweredQuestions()
    question_ids = []
    for question in questions:
        question_ids.append(question['id'])
    return question_ids

def answered_question_list():
    questions = questionDao.getAnsweredQuestions()
    question_ids = []
    for question in questions:
        question_ids.append(question['id'])
    return question_ids

class Question():

    @staticmethod
    def get_question(question_id):
        return questionDao.getQuestionById(question_id)


    @staticmethod
    def get_students_questions(student_id):
        return questionDao.getQuestionsByStudent(student_id)

    @staticmethod
    def add_question(user, question):
        questionDao.addQuestion(user, question)
        pass

    @staticmethod
    def get_questions():
        return questionDao.getQuestions()

    @staticmethod
    def answer_question(question_id, answer):
        questionDao.answerQuestion(question_id, answer)
        pass
