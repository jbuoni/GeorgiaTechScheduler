import pymongo
# Script is expected as follows
# python dbsetup.py 'Path To Resources' 'database name' 'True|False'
# true|false decides which dataset to load. True uses large dataset. False uses small dataset.
from sys import argv as args

db_name = args[2]
resources = args[1]

useLargeFiles=False

coursesfile=resources+'/static/courses.csv'
prereqsfile=resources+'/static/course_dependencies.csv'
semesterfile=resources+'/static/semesters.csv'
usersfile=None
studentrecordsfile=None
instructorpoolfile=None
studentdemand=None

try:
    useLargeFiles= args[3].lower() in ['true']
except:
    print "unable to read argument, defaulting to use smaller dataset."

print useLargeFiles

if useLargeFiles:
    usersfile=resources+'/medium/users_dynamic.csv'
    studentrecordsfile=resources+'/medium/student_records_dynamic.csv'
    instructorpoolfile=resources+'/medium/instructor_TA_pool_dynamic.csv'
    studentdemand=resources+'/medium/student_demand_dynamic.csv'
else:
    usersfile=resources+'/small/users_10.csv'
    studentrecordsfile=resources+'/small/student_records_10.csv'
    instructorpoolfile=resources+'/small/instructor_pool_10.csv'
    studentdemand=resources+'/small/student_demand_10.csv'


conn=pymongo.MongoClient()

db = conn[db_name]

import dbutils

course_collection = db.course
student_collection = db.student
ta_collection = db.ta
prof_collection = db.professor
semester_collection=db.semester
concentration_collection=db.concentration
user_collection=db.user
question_collection=db.question

dbutils.readAndUploadCourses(course_collection,coursesfile,prereqsfile)

print 'loaded courses'

dbutils.readAndUploadSemesters(semester_collection,semesterfile)

print 'loaded semesters'

dbutils.connectCoursesToSemesters(course_collection, semester_collection)

print 'linked courses to semesters'

dbutils.readAndUploadUsers(student_collection, ta_collection, prof_collection, usersfile, studentrecordsfile, instructorpoolfile)

print 'Loaded users'

dbutils.buildConcentrations(concentration_collection)

print 'concentrations created'

dbutils.readAndUploadStudentDemand(student_collection, studentdemand)

print 'student demand uploaded'

dbutils.setupInitialUsers(user_collection, student_collection,ta_collection, prof_collection)

print 'initial users created'

dbutils.createSampleQuestions(question_collection)

print 'sample questions added'
