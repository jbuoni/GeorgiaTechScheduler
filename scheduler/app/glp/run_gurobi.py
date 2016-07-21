
import numpy as np
from gurobipy import *
import pymongo

from ..database import CourseDAO
from ..database import StudentDAO
from ..database import FacultyDAO
from  ..database import GurobiDataGenerator
from ..database import RecommendationDAO
from ..database import ConcentrationDAO

# from ..model import studentDao
# from ..model import courseDao
# from ..model import recommendationDao
# from ..model import concentrationDao


from .. import db


def run_gurobi_model(show_shadow = False):

    # sp = np.random.randint(2, size=(N, C))                 # student_prefernce matrix
    # s_max = np.random.randint(2, 4, size=N)                # student_max courses
    # rank = np.random.choice(N, N, replace=False)           # student_rank
    # cc = np.random.randint(2, size=(N, C))                 # student_preference_core_course
    # c_max = 50*np.ones(C)								     # max_students in a course

    studentDao = StudentDAO.StudentDAO(db)
    facultyDao = FacultyDAO.FacultyDAO(db)
    courseDao = CourseDAO.CourseDAO(db)
    recommendationDao = RecommendationDAO.RecommendationDAO(db)
    concentrationDao = ConcentrationDAO.ConcentrationDAO(db)

    semesterId = 1;

    # getting input matrices
    # student_prefernce matrix
    sp = np.array(GurobiDataGenerator.generateStudentCoursePreferences(semesterId, studentDao, courseDao))
    # student_max courses
    s_max = np.array(GurobiDataGenerator.generateMaxCoursesPerStudent(studentDao))
    # student_preference_core_course
    cc = np.array(GurobiDataGenerator.generateCoreClasses(studentDao ,courseDao, concentrationDao))
    # student_max courses
    c_max = np.array(GurobiDataGenerator.generateCourseCapacity(courseDao, semesterId))
    # student_rank
    rank = np.array(GurobiDataGenerator.generateStudentRank(studentDao))

    N = sp.shape[0]                                        # number of students
    C = sp.shape[1]                                        # total courses offerered next
    w1 = 1                                                 # weight for core course
    w2 = 0.5                                               # weight for core course

    # return student course assignment matrix
    student_assignments = np.zeros([N,C])

    try:
        # create the model
        model = Model("scheduler")
        vars ={}
        # create decision variables
        for i in xrange(N):
            for j in xrange(C):
                if sp[i,j] == 1:
                    vars[i, j] = model.addVar(vtype=GRB.BINARY, name = 'SP' +str(i)+'c'+str(j) )

        #after setting variables update model
        model.update()

        # Populate objective
        obj = 0
        weight = 0
        for i in xrange(N):
            for j in xrange(C):
                if cc[i,j] == 1:
                    weight = w1
                else:
                    weight = w2
                if sp[i,j] == 1:
                    obj += (rank[i]+weight)*vars[i, j]
        model.setObjective(obj, GRB.MAXIMIZE)


        # populate constraints
        # max courses by a student constraint
        for i in xrange(N):
            expr = LinExpr()
            for j in xrange(C):
                if sp[i, j] == 1:
                    expr += vars[i,j]
            model.addConstr(expr, GRB.LESS_EQUAL, s_max[i],'MC'+str(i))


        # model.update()
        # max students in a course
        for i in xrange(C):
            expr = LinExpr()
            for j in xrange(N):
                if sp[j, i] == 1:
                    expr += vars[j,i]
            model.addConstr(expr, GRB.LESS_EQUAL, int(c_max[i]),'CM'+str(i))

        # model.update()
        model.optimize()

        # model.write('scheduler.lp')
        solution = model.getAttr('X', vars)

        for key, value in solution.items():
            i, j = key
            student_assignments[i, j] = value

        #add model recommendations to the database

        courseIds = []
        recommendationDao.clearOutExistingRecommendations()
        for i in xrange(N):
            for j in xrange(C):
                if student_assignments[i,j] == 1:
                    courseIds.append(j+1)
            if len(courseIds) > 0:
                recommendationDao.addRecommendationHistory(i+1, semesterId, courseIds, show_shadow)
            courseIds =[]


    except GurobiError, e:
        print 'error in the gurobi model'
        print e
        return False

    return True

if "__name__=__main__":
    # conn = pymongo.MongoClient()
    # database = conn['CS6310_p3']
    # print database.dataset
    # cursor = database.student.find()
    # for document in cursor:
    #     print(document)
    print ''
    #run_gurobi_model()