
import numpy as np
from gurobipy import *
import pymongo

def generateCourseCapacity(courseDAO, semesterId):
    course_capacity = []
    cursor = courseDAO.findAllCourses()
    for entry in cursor:
        if semesterId in entry['semesters']:
            course_capacity.append(entry['capacity'])
        else:
            course_capacity.append(0)
    return course_capacity


def generateMaxCoursesPerStudent(studentDAO):
    student_max_courses = []
    cursor = studentDAO.findAllStudents()
    for entry in cursor:
        student_max_courses.append(entry['maxcourses'])
           
    return student_max_courses
    
#For now, student 'rank' will consist solely of their seniority. We can consider working in GPA at another time.
def generateStudentRank(studentDAO):
    student_rank = []
    cursor = studentDAO.findAllStudents()
    for entry in cursor:
        student_rank.append(entry['seniority'])
    
    return student_rank

#
def generateStudentCoursePreferences(semesterId, studentDAO, courseDAO):
    student_course_preference = []
    allStudents = studentDAO.findAllStudents()
    for student in allStudents:
        takingCourse = []
        allCourses = courseDAO.findAllCourses()

        for course in allCourses:
            courseMapping = student['requestedcourses']
            if str(semesterId) in courseMapping: #For some reason, Mongo Forces these to be strings. Must compensate.
                classList = courseMapping[str(semesterId)]
            
                if course['courseid'] in classList:
                    takingCourse.append(1)
                else:
                    takingCourse.append(0)
            else:
                takingCourse.append(0)
        student_course_preference.append(takingCourse)
        
    print student_course_preference
    return student_course_preference

def generateCoreClasses(studentDao, courseDAO, concentrationDao):
    core_courses = []
    concentration = {}
    allStudents = studentDao.findAllStudents()
    for student in allStudents:
        isCoreCourse = []
        student_concentration = student['concentration']
        courseMapping = student['requestedcourses']
        x = courseMapping.get("1", None)
        classList = courseMapping.get("1", None) # semesterId = 1
        if student_concentration != None:
            concentration = concentrationDao.get_concentration(student_concentration)

        allCourses = courseDAO.findAllCourses()
        for course in allCourses:

            if classList != None and course['courseid'] in classList:
                if student_concentration == None:
                    isCoreCourse.append(0)
                else:
                    if course['courseid'] in concentration['core']:
                        isCoreCourse.append(1)
                    else:
                        isCoreCourse.append(0)
            else:
                isCoreCourse.append(0)
        core_courses.append(isCoreCourse)
    return core_courses