import pymongo

class UserDAO(object):
    def __init__(self,database):
        self.collection=database.user


    def getUserByUserName(self,username):
        return self.collection.find_one({"id": username})

    def getHashedPW(self, username):
        return self.getUserByUserName(username)['password_hash']

    def isUser(self,username):
        return self.getUserByUserName(username) != None
    
    def isAdmin(self,username):
        user = self.getUserByUserName(username)
        if user != None:
            return user['admin'] == 1
        else:
            return False

    def isDeveloper(self,username):
        user = self.getUserByUserName(username)
        if user != None:
            return user['developer'] == 1
        else:
            return False
