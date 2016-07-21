from flask import g, make_response, jsonify
from flask.ext.httpauth import HTTPBasicAuth
from . import api
from .errors import unauthorized, forbidden
from ..model.user import User
from . import crossDomain

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(user_or_token, password):
    if user_or_token == '':
        pass
    if password == '':
        # check token
        # g.current_user = User.verify_auth_token(user_or_token)
        # g.token_used = True
        return g.current_user is not None
    elif password == User.verify_auth_token(user_or_token):
        return True
    else:
        return False


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')

@api.route('/token')
@crossDomain.crossdomain('*')
def get_token():
    if g.curren_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')

    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})


@auth.login_required
@api.route('/authtest')
@crossDomain.crossdomain('*')
def test_auth():
    return 'authenticated'
