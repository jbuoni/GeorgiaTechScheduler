from flask import make_response, jsonify, url_for, request
from . import api
from . import crossDomain
from ..model.question import Question
from ..model.student import Student
from ..model.course import update_course_list


@api.route('/admin/answer_question', methods=['POST'])
@crossDomain.crossdomain('*')
def put_question_answer():
    Question.answer_question(request.json.get('question').get('id'), request.json.get('question').get('answer'))
    return jsonify({'result': 'OK'})

@api.route('/admin/run_scheduler', methods=['POST'])
@crossDomain.crossdomain('*')
def run_gurobi_scheduler():
    Student.run_solver(False)
    return jsonify({'result': 'OK'})

@api.route('/admin/update_courses', methods=['POST'])
@crossDomain.crossdomain('*')
def put_courses():
    update_course_list(request.json.get('courses'))
    return jsonify({'result': 'OK'})
