from flask.ext.login import UserMixin, AnonymousUserMixin
# from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from .. import login_manager
from ..model import userDao
class Permission:
    STUDENT = 1
    ADMINISTRATOR = 2

unpw = {}
unpw['wpifer3'] = 'pbkdf2:sha1:1000$tpSUiFiT$7f3c6df0b61c29fe1e36badc00b6d290c4529134'
unpw['jbuoni3'] = 'pbkdf2:sha1:1000$R3ERQZ3v$b506425ab7091cd4f2eef73d492fc824035d78c4'
unpw['kniemczyk3'] = 'pbkdf2:sha1:1000$bbOAAVEh$361e0c15b21eee184d073e407c0dbad354cd2a3b'
unpw['vdhogadugu3'] = 'pbkdf2:sha1:1000$5Y95GE1j$23541cf4879812ca08d595b20be635fbe9b162df'

user_info = {}

user_info['wpifer3'] = {'name': 'Wendy', 'developer': 1, 'admin': 0}
user_info['jbuoni3'] = {'name': 'Jason', 'developer': 1, 'admin': 0}
user_info['kniemczyk3'] = {'name': 'Kevin', 'developer': 1, 'admin': 0}
user_info['vdhogadugu3'] = {'name': 'Venkat', 'developer': 1, 'admin': 0}

def user_list():
    return user_info.keys()

class User(UserMixin):
    def __init__(self, user_name):
        self.id = user_name
        pass

    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        #return check_password_hash(self.password_hash, password)
        return check_password_hash(userDao.getHashedPW(self.id), password)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('ascii')

    def get_info(self, user_name):
        #return user_info[user_name]
        return userDao.getUserByUserName(user_name)

    @staticmethod
    def is_admin(user_name):
        #return user_info[user_name]['admin'] == 1
        return userDao.isAdmin(user_name)

    @staticmethod
    def is_developer(user_name):
        # return user_info[user_name]['admin'] == 1
        return userDao.isDeveloper(user_name)

    @staticmethod
    def is_user(user_name):
#         if user_name in unpw.keys():
#             return True
#         else:
#             return False
        return userDao.isUser(user_name)

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return user(data['id'])

class user():
    pass

@login_manager.user_loader
def load_user(user_name):
    return User(user_name)
