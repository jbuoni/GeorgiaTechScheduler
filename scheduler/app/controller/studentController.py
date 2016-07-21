from ..model.student import Student
from ..model.course import Course, course_list
from ..model.question import Question
from ..model.concentration import Concentration


class StudentData:
    pass

class CourseViewObject(object):
    course_id = -1
    name = ""

def get_student_info(username):
    studentId = int(Student.get_info(username)['userid'])
    StudentData.student_info = Student.get_info(username)
    con = Student.get_specialization(username)
    if con is None:
        StudentData.specialization = "No concentration chosen"
    else:
        value = Concentration.get_concentration_name(Student.get_specialization(username))
        if value is None: 
            StudentData.specialization = "No concentration chosen"
        else:
            StudentData.specialization = str(Concentration.get_concentration_name(Student.get_specialization(username))),
    
    StudentData.completed_courses = get_completed_courses(StudentData.student_info)
    StudentData.course_preferences = get_course_preferences(StudentData.student_info, "1")
    StudentData.courses = get_courses()
    StudentData.questions = Question.get_students_questions(username)
    StudentData.semester = "1"
    
    StudentData.solutions = get_student_recommendations(studentId, False)
    return StudentData


def get_completed_courses(student):
    completed_courses = []
    for course_id in student['completed']:
        completed_courses.append(Course.get_course(course_id))
    return completed_courses


def get_course_preferences(student, semester):
    course_preferences = []
    requested = student['requestedcourses']
    if requested is None:
        return course_preferences
    if str(semester) not in requested:
        return course_preferences
    else:
        for course_id in student['requestedcourses'][str(semester)]:
            course_preferences.append(Course.get_course(int(course_id)))
    return course_preferences

def get_courses():
    #TODO when courses are added, this needs to be updated
    courselist = []

    courses = course_list()

    for key in courses:
        courselist.append(Course.get_course(key))

    return courselist


def get_student_recommendations(user_id, show_shadow):
    course_recommendations = []
    recos  = Student.get_student_recommendations(user_id, show_shadow)
    if (recos != None):
        for course_id in recos:
            course_recommendations.append(Course.get_course(int(course_id)))
    return course_recommendations


def run_gurobi_model(show_shadow):
    return Student.run_solver(show_shadow)


