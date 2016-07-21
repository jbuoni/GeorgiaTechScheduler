from flask import make_response, jsonify, url_for, request
from . import api
from . import crossDomain
from ..model.course import Course, course_list


@api.route('/courses')
@crossDomain.crossdomain('*')
def get_course_list():
    courses = course_list()
    course_dict = {}
    for id in courses:
        course_dict[id] = url_for('api.get_course', course_id=id, _external=True)
    return jsonify({'users list': course_dict})


@api.route('/courses/<string:course_id>')
@crossDomain.crossdomain('*')
def get_course(course_id):
    return jsonify({'course id': course_id, 'course': Course.get_course(course_id)})


@api.route('/courses/<string:course_id>/description')
@crossDomain.crossdomain('*')
def get_course_description(course_id):
    return jsonify({'course id': course_id, 'description': Course.get_description(course_id)})


@api.route('/courses/<string:course_id>/capacity')
@crossDomain.crossdomain('*')
def get_course_capacity(course_id):
    return jsonify({'course id': course_id, 'capacity': Course.get_capacity(course_id)})


@api.route('/courses/<string:course_id>/enrollment')
@crossDomain.crossdomain('*')
def get_course_enrollment(course_id):
    return jsonify({'course id': course_id, 'enrollment': Course.get_enrollment(course_id)})


@api.route('/courses/<string:course_id>/availability')
@crossDomain.crossdomain('*')
def get_course_availability(course_id):
    return jsonify({'course id': course_id, 'availability': Course.get_availability(course_id)})


@api.route('/courses/<string:course_id>/professors')
@crossDomain.crossdomain('*')
def get_course_professors(course_id):
    return jsonify({'course id': course_id, 'professors': Course.get_professors(course_id)})


@api.route('/courses/<string:course_id>/prereqs')
@crossDomain.crossdomain('*')
def get_course_prereqs(course_id):
    return jsonify({'course id': course_id, 'prereqs': Course.get_prereqs(course_id)})


@api.route('/courses/<string:course_id>', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course(course_id):
    Course.put_course(course_id, request.json.get('course'))


@api.route('/courses/<string:course_id>/description', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course_description(course_id):
    Course.put_description(course_id, request.json.get('description'))


@api.route('/courses/<string:course_id>/capacity', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course_capacity(course_id):
    Course.put_capacity(course_id, request.json.get('capacity'))


@api.route('/courses/<string:course_id>/enrollment', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course_enrollment(course_id):
    Course.put_enrollment(course_id, request.json.get('enrollment'))


@api.route('/courses/<string:course_id>/availability', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course_availability(course_id):
    Course.put_description(course_id, request.json.get('availability'))


@api.route('/courses/<string:course_id>/professors', methods=['POST'])
@crossDomain.crossdomain('*')
def put_course_professors(course_id):
    Course.put_description(course_id, request.json.get('professors'))

