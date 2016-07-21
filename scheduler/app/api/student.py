from flask import make_response, jsonify, url_for, request
from . import api
from . import crossDomain
from ..model.student import Student, students_list
from ..model.question import Question


@api.route('/students')
@crossDomain.crossdomain('*')
def get_students_list():
    students = students_list()
    student_dict = {}
    for name in students:
        student_dict[name] = url_for('api.get_student', studentname=name, _external=True)
    return jsonify({'students list': student_dict})


@api.route('/students/<string:studentname>')
@crossDomain.crossdomain('*')
def get_student(studentname):
    return jsonify({'student': studentname, 'student info': Student.get_info(studentname)})


@api.route('/students/<string:studentname>/specialization')
@crossDomain.crossdomain('*')
def get_student_specialization(studentname):
    return jsonify({'student': studentname, 'specialization': Student.get_specialization(studentname)})


@api.route('/students/<string:studentname>/specialization', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_specialization(studentname):
    Student.put_specialization(studentname, request.json.get('specialization'))


@api.route('/students/<string:studentname>/credits')
@crossDomain.crossdomain('*')
def get_student_credits(studentname):
    return jsonify({'student': studentname, 'credits': Student.get_credits(studentname)})


@api.route('/students/<string:studentname>/credits', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_credits(studentname):
    Student.put_credits(studentname, request.json.get('credits'))


@api.route('/students/<string:studentname>/gpa')
@crossDomain.crossdomain('*')
def get_student_gpa(studentname):
    return jsonify({'student': studentname, 'gpa': Student.get_gpa(studentname)})


@api.route('/students/<string:studentname>/gpa', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_gpa(studentname):
    Student.put_gpa(studentname, request.json.get('gpa'))


@api.route('/students/<string:studentname>/graduation')
@crossDomain.crossdomain('*')
def get_student_graduation(studentname):
    return jsonify({'student': studentname, 'graduation': Student.get_graduation()})


@api.route('/students/<string:studentname>/graduation', methods=['POST'])
@crossDomain.crossdomain('*')
def set_student_graduation(studentname):
    Student.put_graduation(studentname, request.json.get('graduation'))


@api.route('/students/<string:studentname>/completed')
@crossDomain.crossdomain('*')
def get_student_courses_completed(studentname):
    completed = Student.get_courses_completed(studentname)
    course_dict = {}
    for course in completed:
        course_dict[course] = url_for('api.get_course', course_id=course, _external=True)
    return jsonify({'student': studentname, 'completed courses': course_dict})


@api.route('/students/<string:studentname>/completed', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_courses_completed(studentname):
    Student.put_courses_compeleted(studentname, request.json.get('completed courses'))


@api.route('/students/<string:studentname>/requested')
@crossDomain.crossdomain('*')
def get_student_courses_requested(studentname):
    requested = Student.get_courses_requested(studentname)
    requested_dict = {}
    for course in requested:
        requested_dict[course] = url_for('api.get_course', course_id=course, _external=True)
    return jsonify({'student': studentname, 'completed courses': requested_dict})


@api.route('/students/<string:studentname>/requested', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_courses_requested(studentname):
    Student.put_courses_requested(studentname, request.json.get('requested courses'))


@api.route('/students/<string:studentname>/preferences', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_preferences(studentname):
    stringified_courses = request.json.get('preferences').get('courseIDs')
    real_courses = []
    for item in stringified_courses: real_courses.append(int(item)) 
    Student.put_courses_requested(studentname, request.json.get('preferences').get('semester'), real_courses)
    return jsonify({'result': 'OK'})


@api.route('/students/<string:studentname>/question', methods=['POST'])
@crossDomain.crossdomain('*')
def put_student_questions(studentname):
    question = request.json.get('question')
    Question.add_question(studentname, question)
    return jsonify({'result': 'OK'})
