from ..model.user import User

class authData:
    name = ""
    isAdmin = False
    isStudent = False
    isDeveloper = False

def get_auth_data(username):
    authData.name = username
    authData.isAdmin = User.is_admin(username) == 1
    authData.isDeveloper = User.is_developer(username) == 1
    authData.isStudent = (not authData.isAdmin or authData.isDeveloper)
    return authData