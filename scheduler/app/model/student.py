student_info = {}

student_info['wpifer3'] = {
    'name': 'Wendy Pifer',
    'specialization': 'interactive intelligence',
    'credits_earned': 3,
    'gpa': 4.0,
    'completed': ['17'],
    'requested': ['5', '23'],
    'graduation': 'FALL 2017'
}

student_info['jbuoni3'] = {
    'name': 'Jason Buoni',
    'specialization': 'Computing Systems',
    'credits_earned': 0,
    'gpa': '',
    'completed': ['17', '4'],
    'requested': ['5', '3'],
    'graduation': 'Spring 2018'
}

student_info['kniemczyk'] = {
    'name': 'Kevin Niemczyk',
    'specialization': 'computing systems',
    'credits_earned': 0,
    'gpa': '',
    'completed': [],
    'requested': ['5', '3'],
    'graduation': 'SPRING 2018'
}

student_info['vdhomadugu3'] = {
    'name': 'Venkateshwar Dhomadugu',
    'specialization': 'computing systems',
    'credits_earned': 0,
    'gpa': 4.0,
    'completed': [],
    'requested': ['5', '3'],
    'graduation': 'SPRING 2018'
}


from ..model import courseDao
from ..model import studentDao
from ..model import semesterToUse
from ..model import facultyDao
from ..model import recommendationDao
from ..glp import run_gurobi


def students_list():
    students = studentDao.findAllStudents()
    student_ids = []
    for student in students:
        student_ids.append(student['username'])
    return student_ids


#####NOTE: user_id in all the static calls ARE THE USERNAME!
class Student():

    @staticmethod
    def get_name(user_name):
        print 'username: ' + user_name
        entry = studentDao.findStudentByUsername(user_name)
        return (entry['firstname'], entry['lastname'])


    @staticmethod
    def get_info(user_name):
        ##FOR NOW, ASSUME ALL USERS ARE STUDENTS
        return studentDao.findStudentByUsername(user_name)

    @staticmethod
    def get_specialization(user_name):
        return studentDao.findStudentByUsername(user_name)['concentration']
        

    @staticmethod
    def get_gpa(user_name):
        return studentDao.findStudentByUsername(user_name)['gpa']

    @staticmethod
    def get_credits(user_name):
        return studentDao.findStudentByUsername(user_name)['credits_earned']

    @staticmethod
    def get_dept_id(user_name):
        return studentDao.findStudentByUsername(user_name)['deptid']

    @staticmethod
    def get_courses_completed(user_name):
        result = studentDao.findStudentByUsername(user_name)
        if result is None: return []
        else: return result['completed']

    @staticmethod
    def get_courses_requested(user_name):
        requested = studentDao.findStudentByUsername(user_name)['requestedcourses']
        if requested is None : return []
        else: 
            courses = requested[str(semesterToUse)]
            if courses is None : return []
            else: return courses

    @staticmethod
    def get_graduation(user_name):
        #KJN: Not sure what to do here?
        student = studentDao.findStudentByUsername(user_name)
        return student['graduation']

    @staticmethod
    def put_specialization(user_name, specialization):
        #user_info[user_name]['specialization'] = specialization
        #NOTE: KJN -- Specialization in this point IS THE ID OF THE CONCENTRATION!
        studentDao.setUserConcentrationByUsername(user_name, specialization)

    @staticmethod
    def put_gpa(user_name, gpa):
        studentDao.setGPAByUsername(user_name, gpa)

    @staticmethod
    def put_credits(user_name, credits_earned):
        studentDao.setCreditsEarnedByUsername(user_name, credits_earned)
        
    @staticmethod
    def put_courses_completed(user_name, completed):
        studentDao.setCoursesCompletedByUsername(user_name,completed)

    @staticmethod
    def complete_course(user_name, completed_course_id):
        studentDao.addCompletedCourse(user_name, completed_course_id)

    @staticmethod
    def put_courses_requested(user_name, semester, requested):
        studentDao.setPreferredCoursesByUsername(user_name, semester, requested)

    @staticmethod
    def put_graduation(user_name, graduation):
        studentDao.setGraduationByUsername(user_name, graduation)


    @staticmethod
    def find_all_students():
        return studentDao.findAllStudents()

    @staticmethod
    def get_student_recommendations(user_id, show_shadow):
        return recommendationDao.findRecommendationsForStudentById(user_id, show_shadow)

    @staticmethod
    def get_all_students_recommendations(show_shadow):
        return recommendationDao.findAllStudentRecommendations(show_shadow)

    @staticmethod
    def run_solver(show_shadow):
        return run_gurobi.run_gurobi_model(show_shadow)




    

