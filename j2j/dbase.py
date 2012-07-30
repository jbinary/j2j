import shelve

class UserBase(object):

    def __init__(self, path):
        self.base = shelve.open(path)

    def addUser(self, key, name, pswrd):
        self.base[key] = name, pswrd

    def removeUser(self, key):
        del self.base[key]

    def keyInBase(self, key):
        return key in self.base.keys()

    def userInBase(self, user):
        for u in self.base.values():
            if u[0] == user:
                return True
        return False

    def getUser(self, key):
        return self.base[key]
