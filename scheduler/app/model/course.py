courses = {}

courses['0'] = 'Introduction to Information Security'
courses['1'] = 'Advanced Operating Systems'
courses['2'] = 'Intro to High-Performance Computing'
courses['3'] = 'Computer Networks'
courses['4'] = 'High Performance Computer Architecture'
courses['5'] = 'Software Development Process'
courses['6'] = 'Software Architecture and Design'
courses['7'] = 'Software Analysis and Test'
courses['8'] = 'Database Systems Concepts and Design'
courses['9'] = 'Intro to Health Informatics'
courses['10'] = 'Educational Technology'
courses['11'] = 'Computational Photography'
courses['12'] = 'Computer Vision'
courses['13'] = 'Computability, Complexity and Algorithms'
courses['14'] = 'Artificial Intelligence'
courses['15'] = 'Knowledge-Based Artificial Intelligence: Cognitive Systems'
courses['16'] = 'Machine Learning'
courses['17'] = 'Machine Learning for Trading'
courses['18'] = 'Special Topics: Big Data for Health Informatics'
courses['19'] = 'Artificial Intelligence for Robotics'
courses['20'] = 'Introduction to Operating Systems'
courses['21'] = 'Special Topics: Reinforcement Learning'
courses['22'] = 'Special Topics: Embedded Software'
courses['23'] = 'Network Security'

course_number = {}
course_number['0'] = 'CS 6035'
course_number['1'] = 'CS 6210'
course_number['2'] = 'CSE 6220'
course_number['3'] = 'CS 6250'
course_number['4'] = 'CS 6290'
course_number['5'] = 'CS 6300'
course_number['6'] = 'CS 6310'
course_number['7'] = 'CS 6340'
course_number['8'] = 'CS 6400'
course_number['9'] = 'CS 6440'
course_number['10'] = 'CS 6460'
course_number['11'] = 'CS 6475'
course_number['12'] = 'CS 6476'
course_number['13'] = 'CS 6505'
course_number['14'] = 'CS 6601'
course_number['15'] = 'CS 7637'
course_number['16'] = 'CS 7641'
course_number['17'] = 'CS 7646'
course_number['18'] = 'CSE 8803'
course_number['19'] = 'CS 8803-O01'
course_number['20'] = 'CS 8803-O02'
course_number['21'] = 'CS 8803-O03'
course_number['22'] = 'CS 8803-O04'
course_number['23'] = 'CS 6262'

course_availability = {'fall': True,
                       'spring': True,
                       'summer': False}

course_profs = ['professor buoni', 'professor niemczyk', 'professor venkat']

course_capacity = 300

course_enrollment = 217

course_description = 'this is a description of a coursey course'

course_prereqs = ['0','5']

# DATABASE = None

#KJN
from ..database import FacultyDAO

from ..model import courseDao
from ..model import studentDao
from ..model import semesterToUse
from ..model import facultyDao


def course_list():
    courses = courseDao.findAllCourses()
    course_ids = []
    for course in courses:
        course_ids.append(course['courseid'])
    return course_ids

def update_course_list(courses):
    for course in courses:
        courseDao.setCourseCapacity(int(course['id']), course['capacity'])
        courseDao.setCourseFallTerm(int(course['id']), course['fallTerm'])
        courseDao.setCourseSpringTerm(int(course['id']), course['springTerm'])
        courseDao.setCourseSummerTerm(int(course['id']), course['summerTerm'])
        courseDao.setCourseAvaiability(int(course['id']), course['availability'])


class Course(object):

    @staticmethod
    def get_course(course_id):
        # in the future this should return all course info
        #  course_dict = {'coursename': courses[course_id],
        #                 'coursenumber': course_number[course_id],
        #                 'description': course_description,
        #                 'capacity': course_capacity,
        #                 'enrollment': course_enrollment,
        #                 'availability': course_availability,
        #                 'professors': course_profs,
        #                 'prereqs': course_prereqs}
        #  return course_dict
        return courseDao.findCourseById(course_id)

    @staticmethod
    def get_description(course_id):
        #return course_description
        return courseDao.findCourseById(course_id)['coursename']

    @staticmethod
    def get_capacity(course_id):
        #return course_capacity
        return courseDao.findCourseById(course_id)['capacity']

    @staticmethod
    def get_enrollment(course_id):
        ##KJN: Not sure what this is - System is not responsible for enrollment
        #The best I think we could do would be to find the number of students
        #who are requesting this course for a specific semester.
        #return course_enrollment
        return studentDao.findInterest(course_id, semesterToUse)

    @staticmethod
    def get_availability(course_id):
        #What do we want to do here? Return the semesters it is available? or just
        #the string description? For now I'm doing the latter.
        #return course_availability
        return courseDao.findCourseById(course_id)['availability']

    @staticmethod
    def get_professors(course_id):
        
        #return course_profs
        return facultyDao.findFacultyForCourseSemester(FacultyDAO.FacultyDAO.PROF_ONLY, course_id, semesterToUse)

    @staticmethod
    def get_prereqs(course_id):
        #return course_prereqs
        return courseDao.findCourseById(course_id)['prereq']
    
    @staticmethod
    def get_concentrations():
        return courseDao.findAllConcentrations()

    #KJN: Not sure we need the calls below for initial implementation.
    @staticmethod
    def put_course(course_id, course_data):
        courses[course_id] = course_data

    @staticmethod
    def put_description(course_id, description):
        course_description = description

    @staticmethod
    def put_capacity(course_id, capacity):
        courseDao.setCourseCapacity(course_id, capacity)

    @staticmethod
    def put_enrollment(course_id, enrollment):
        course_enrollment = enrollment

    @staticmethod
    def put_availability(course_id, availability):
        course_availability = availability

    @staticmethod
    def put_professors(course_id, professors):
        course_profs = professors
    
    @staticmethod
    def add_semester(course_id, semester_id):
        courseDao.addSemesterAvailable(course_id,semester_id)
    
    @staticmethod
    def remove_semester(course_id, semester_id):
        courseDao.removeSemesterAvailable(course_id,semester_id)
        
class semester():
    pass

class professor():
    pass

