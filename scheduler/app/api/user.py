from flask import make_response, jsonify, url_for, request
from . import api
from . import crossDomain
from ..model.user import User, user_list


@api.route('/users')
@crossDomain.crossdomain('*')
def get_user_list():
    users = user_list()
    user_dict = {}
    for name in users:
        user_dict[name] = url_for('api.get_users', username=name, _external=True)
    return jsonify({'students list': user_dict})


@api.route('/users/<string:username>')
@crossDomain.crossdomain('*')
def get_user(username):
    return jsonify({'username': username, 'user info': User.get_info(User(username), username)})

