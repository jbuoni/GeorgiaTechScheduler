import csv
#Dummy class for dynamically building data to load into mongo
class DBLoader:
    def __init__(self):
        pass;


#Put this in a function for processing the file and adding into mongodb document
#This takes the user_dynamic.csv file or users_10.csv file
def readAndUploadUsers(students, teachingassistents,professors, userfilepath,studentrecordpath,instructorpoolpath):
    student_entries = {}
    ta_entries={}
    prof_entries={}
    with open(userfilepath, 'rU') as csvfile:
        userreader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(userreader,None)
        for row in userreader:
            data = DBLoader()
            data.userid = int(row[0])
            data.firstname=row[1]
            data.lastname=row[2]
            data.username=row[3]
            data.deptid=int(row[4])
            data.roleid=int(row[5])
            
            if data.roleid != 5:
                data.course_semester=[]
            
            
            if int(data.roleid) == 5: 
                #Set initial default 2 of max courses a student is allowed to take per semester
                data.maxcourses=2
                #By default, set student concentration to None. Can be set later.
                data.concentration=None
                #By default set student demand to empty dict
                data.requestedcourses={}
                data.completed=[]
                data.enrolled=[]
                data.seniority = 0
                data.gpa = 0.0
                data.graduation=None
                data.credits_earned=0
                
                student_entries[data.userid]=data
            elif int(data.roleid) == 1 : ta_entries[data.userid]=data
            elif int(data.roleid) == 3 : prof_entries[data.userid]=data

    with open(studentrecordpath, 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(reader,None)
        for row in reader:
            item = student_entries[int(row[0])]
            item.seniority = int(row[1])
            item.gpa = float(row[2])
            student_entries[item.userid] = item
    with open(instructorpoolpath, 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(reader,None)
        for row in reader:
            data = DBLoader()
            data.id=int(row[0])
            data.course_id=int(row[1])
            data.role=int(row[2])
            data.semester=int(row[3])
            if data.role == 3:
                item = prof_entries[data.id]
                item.course_semester.append((data.course_id, data.semester))
                prof_entries[data.id]=item
            elif data.role == 1:
                item = ta_entries[data.id]
                item.course_semester.append((data.course_id, data.semester))
                ta_entries[data.id]=item
    
#    if len(student_entries) > 0 : student.insert_many(student_entries)
#    if len(ta_entries) > 0 : teachingassistents.insert_many(ta_entries)
#    if len(prof_entries) > 0 : professors.insert_many(prof_entries)
    for key in student_entries:
        students.insert(student_entries[key].__dict__)
    for key in ta_entries:
        teachingassistents.insert(ta_entries[key].__dict__)

        #Wendy pointed out a good point that TAs are student too. So I'm adding them into both collections. The only
        #real difference between the two is that TAs will have this course_semester list
        #which indicates the courses and semesters they are teaching.
        #students.insert(ta_entries[key].__dict__)
    for key in prof_entries:
        professors.insert(prof_entries[key].__dict__)

                


#This reads course file and course_dependency files.
def readAndUploadCourses(collection, coursepath, coursedependencypath):
    courses = {}
    with open(coursepath, 'rU') as csvfile:
        coursereader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(coursereader,None)
        for row in coursereader:
            data = DBLoader()
            data.courseid=int(row[0])
            data.coursename=row[1]
            data.coursenumber=row[2]
            data.fallterm=int(row[3])
            data.springterm=int(row[4])
            data.summerterm=int(row[5])
            data.availability=row[6]
            data.semesters=[]
            
            #For now, set a default of 50 for course capacity. This can be changed later via admin
            data.capacity = 50
            
            courses[data.courseid]=data

    with open(coursedependencypath, 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(reader,None)
        for row in reader:
            
            prereq = int(row[0])
            dependent = int(row[1])
            item = courses[dependent]
            item.prereq = prereq
            courses[dependent]=item


    for key in courses:
        collection.insert(courses[key].__dict__)

def readAndUploadSemesters(collection, semesterpath):
    with open(semesterpath, 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab,delimiter=',')
        sems = []
        next(reader,None)
        for row in reader:
            data = DBLoader()
            data.semester=int(row[0])
            data.semester_name=row[1]
            data.start_date=row[2]
            data.end_date=row[3]
            sems.append(data.__dict__)
        collection.insert_many(sems)

#Note, these concentrations will be hardwired for now.
#They're also completely artificial since the specializations on the OMS CS website
#don't really correspond to what is in the data sample set. We can adjust later as need be
def buildConcentrations(collection):
    collection.insert({'id' : 1, 'name': 'Computation Perception and Robotics','core':[13,9,10,11]})
    collection.insert({'id' : 2, 'name': 'Computing Systems','core':[3,6,1,5]})
    collection.insert({'id' : 3, 'name': 'Interactive Intelligence','core':[13,9,17]})
    collection.insert({'id' : 4, 'name': 'Machine Learning','core': [4,16, 18]})


def connectCoursesToSemesters(course_collection, semester_collection):
    fall=[]
    spring=[]
    summer=[]
    for cursor in semester_collection.find():
        if cursor['semester_name'].startswith('Fall'):
            fall.append(cursor['semester'])
        elif cursor['semester_name'].startswith('Spring'):
            spring.append(cursor['semester'])
        elif cursor['semester_name'].startswith('Summer'):
            summer.append(cursor['semester'])

    for cursor in course_collection.find({"fallterm":1}):
        mylist = cursor['semesters']
        mylist.extend(fall)
        course_collection.update({"_id":cursor['_id']},{"$set":{'semesters':mylist}})
    for cursor in course_collection.find({"springterm":1}):
        mylist = cursor['semesters']
        mylist.extend(spring)
        course_collection.update({"_id":cursor['_id']},{"$set":{'semesters':mylist}})
    for cursor in course_collection.find({"summerterm":1}):
        mylist = cursor['semesters']
        mylist.extend(summer)
        course_collection.update({"_id":cursor['_id']},{"$set":{'semesters':mylist}})

def readAndUploadStudentDemand(student_collection, demandfile):
    studentDemandDict = {}
    with open(demandfile, 'rU') as csvfile:
        reader = csv.reader(csvfile,dialect=csv.excel_tab, delimiter=',')
        next(reader,None)
        for row in reader:
            student = row[0]
            course = int(row[1])
            semester = row[2]
            semesterCourseMap={}
            if student in studentDemandDict:
                semesterCourseMap = studentDemandDict[student]
            
            if semester in semesterCourseMap:
                current = semesterCourseMap[semester]
                current.append(course)
                semesterCourseMap[semester]=current
            else:
                current = []
                current.append(course)
                semesterCourseMap[semester]=current

            studentDemandDict[student] = semesterCourseMap


    #post reading, now insert into student collection
    for key in studentDemandDict:
        #Key is the student id so match on that
        cursor = student_collection.find({'userid':int(key)})
        for doc in cursor:  
            student_collection.update({"_id":doc['_id']}, {"$set":{'requestedcourses': studentDemandDict[key]}})


def setupInitialUsers(user_collection,student_collection,ta_collection, prof_collection):
    
    #Setup developers.
    unpw = {}
    unpw['wpifer3'] = 'pbkdf2:sha1:1000$tpSUiFiT$7f3c6df0b61c29fe1e36badc00b6d290c4529134'
    unpw['jbuoni3'] = 'pbkdf2:sha1:1000$R3ERQZ3v$b506425ab7091cd4f2eef73d492fc824035d78c4'
    unpw['kniemczyk3'] = 'pbkdf2:sha1:1000$bbOAAVEh$361e0c15b21eee184d073e407c0dbad354cd2a3b'
    unpw['vdhogadugu3'] = 'pbkdf2:sha1:1000$5Y95GE1j$23541cf4879812ca08d595b20be635fbe9b162df'
    
    user_info = {}
    
    user_info['wpifer3'] = {'id' : 'wpifer3', 'name': 'Wendy', 'developer': 1, 'admin': 0, 'password_hash' : unpw['wpifer3']}
    user_info['jbuoni3'] = {'id' : 'jbuoni3', 'name': 'Jason', 'developer': 1, 'admin': 0, 'password_hash' : unpw['jbuoni3']}
    user_info['kniemczyk3'] = {'id' : 'kniemczyk3', 'name': 'Kevin', 'developer': 1, 'admin': 0, 'password_hash' : unpw['kniemczyk3']}
    user_info['vdhogadugu3'] = {'id' : 'vdhogadugu3','name': 'Venkat', 'developer': 1, 'admin': 0, 'password_hash' : unpw['vdhogadugu3']}
    for item in user_info:
        user_collection.insert(user_info[item])
    
    #Now setup appropriate user information for all students
    
    for cursor in student_collection.find():
        data = {'id' : cursor['username'], 'name' : cursor['firstname'], 'developer' : 0, 'admin' : 0, 'password_hash' : 'pbkdf2:sha1:1000$wkz2AREW$b734c064f090c36eb97372ec95da7ac705618bf1'}
        user_collection.insert(data)
        
    #Now setup appropriate user info for tas and professors.
    for cursor in ta_collection.find():
        data = {'id' : cursor['username'], 'name' : cursor['firstname'], 'developer' : 0, 'admin' : 1, 'password_hash' : 'pbkdf2:sha1:1000$wkz2AREW$b734c064f090c36eb97372ec95da7ac705618bf1'}
        user_collection.insert_one(data)
        
    for cursor in prof_collection.find():
        data = {'id' : cursor['username'], 'name' : cursor['firstname'], 'developer' : 0, 'admin' : 1, 'password_hash' : 'pbkdf2:sha1:1000$wkz2AREW$b734c064f090c36eb97372ec95da7ac705618bf1'}
        user_collection.insert_one(data)    
    
    

def createSampleQuestions(question_collection):
    from datetime import datetime
    q1 = {'id' : 1, "user_id" : 1, "question" : "Why did the chicken cross the road?", 
          "answer" : "Because RuntimeException", "timestamp" : datetime.now()}
    q2 = {'id' : 2, "user_id" : 2, "question" : "Do you plan to take summer classes?", "timestamp" : datetime.now()}
    q3 = {'id' : 3, "user_id" : 2, "question" : "What does a cat eat for dessert?", "answer" : "A Mice-Cream cone!", "timestamp" : datetime.now()}
    q4 = {'id': 4, "user_id" : 3, "question" : "Do you want ants?", "answer" : "This is how you get ants!", "timestamp": datetime.now()}
    q5 = {'id': 5, "user_id" : 4, "question" : "Plate or platter?", "answer" : "I don't understand the question, and I won't respond to it", "timestamp": datetime.now()}
    q6 = {'id': 6, "user_id" : 5, "question" : "Listen, can you smell that?", "timestamp": datetime.now()}
    q7 = {'id': 7, "user_id" : 6, "question" : "Are we not doing phrasing anymore?", "timestamp": datetime.now()}
    q8 = {'id': 8, "user_id" : 7, "question" : "It's one banana, Michael. What could it cost? Ten dollars?", "timestamp": datetime.now()}
    question_collection.insert(q1)
    question_collection.insert(q2)
    question_collection.insert(q3)
    question_collection.insert(q4)
    question_collection.insert(q5)
    question_collection.insert(q6)
    question_collection.insert(q7)
    question_collection.insert(q8)
