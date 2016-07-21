from ..model.course import Course, course_list
from ..model.student import students_list, Student
from ..model.question import unanswered_question_list, answered_question_list, Question
from ..model.concentration import Concentration


class CourseAggregateData:
    courses = []

class StudentListData:
    students = []

class QuestionsData:
    answeredQuestions = []
    unansweredQuestions = []


def get_course_aggregate_data():
    courseList = course_list()
    courses = []
    course_request = calculate_student_demand()
    courses_recommended = calculate_students_recommended()

    for courseId in courseList:
        course = Course.get_course(courseId)
        if course_request == None:
            requestedCourse = 0
        else :
            requestedCourse = course_request[courseId]

        if courses_recommended == None:
            recommendedCourse = 0
        else:
            recommendedCourse = courses_recommended[courseId]

        courses.append({'id': courseId,
                        'number': course['coursenumber'],
                        'name': course['coursename'],
                        'enrollment': requestedCourse,
                        'recommended': recommendedCourse,
                        'max_capacity': course['capacity']
                        })

    retData = CourseAggregateData
    retData.courses = courses
    return retData


def get_schedule_data():
    courseList = course_list()
    courses = []

    course_request = calculate_student_demand()

    for courseId in courseList:
        course = Course.get_course(courseId)
        courses.append({'id': courseId,
                        'number': course['coursenumber'],
                        'name': course['coursename'],
                        'requests': course_request[courseId],
                        'max_capacity': course['capacity'],
                        'offered': course['fallterm'],
                        'ta_pool': int(course['capacity']) / 50,
                        'professor': 'Not Assigned'
                        })
    retData = CourseAggregateData
    retData.courses = courses
    return retData


def get_student_list():
    students = students_list()
    data = []
    for student in students:
        # data.append(Student.get_info(student))
        name = Student.get_name(student)

        data.append({'id': student,
                     'firstname': name[0],
                     'lastname': name[1],
                     'specialization': Concentration.get_concentration_name(Student.get_specialization(student)),
                     'credits': Student.get_credits(student),
                     'deptId': Student.get_dept_id(student),
                     'graduation': Student.get_graduation(student),
                     'gpa': Student.get_gpa(student)})
    retData = StudentListData
    retData.students = data
    return retData

def get_questions_list():
    retData = QuestionsData
    retData.unansweredQuestions=[]
    retData.answeredQuestions=[]
    unanswered_question_ids = unanswered_question_list()
    answered_question_ids = answered_question_list()

    for unanswered_question_id in unanswered_question_ids:
        retData.unansweredQuestions.append(Question.get_question(unanswered_question_id))

    for answered_question_id in answered_question_ids:
        retData.answeredQuestions.append(Question.get_question(answered_question_id))

    return retData

def calculate_student_demand():
    course_dictionary = {}
    students = Student.find_all_students()
    semesterId = 1


    for courseId in course_list():
        course_dictionary[courseId] = 0

    for student in students:
        #Update courses
        courseMapping = student['requestedcourses']

        #course_recommendations = Student.get_student_recommendations(int(student['userid']), False)

        # if course_recommendations == None:
        #     return None
        #
        # for course_id in course_recommendations:
        #     course_dictionary[int(course_id)] = course_dictionary[int(course_id)] + 1

        if str(semesterId) in courseMapping:
            for course_id in courseMapping[str(semesterId)]:
                course_dictionary[int(course_id)] = course_dictionary[int(course_id)] + 1

    return course_dictionary

def calculate_students_recommended():
    course_dictionary = {}
    students = Student.find_all_students()
    semesterId = 1

    for courseId in course_list():
        course_dictionary[courseId] = 0

    for student in students:
        # Update courses
        courseMapping = student['requestedcourses']

        course_recommendations = Student.get_student_recommendations(int(student['userid']), False)

        if course_recommendations == None:
            return None

        for course_id in course_recommendations:
            course_dictionary[int(course_id)] = course_dictionary[int(course_id)] + 1

    return course_dictionary

def get_all_student_recommentations(show_shadow):
    return Student.get_student_recommendations(show_shadow)


def run_gurobi_model(show_shadow):
    return Student.run_solver(show_shadow)





