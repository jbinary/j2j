import shelve

class UserBase(object):

    def __init__(self, path):
        self.base = shelve.open(path)

    def addUser(self, key, name, pswrd):
        self.base[key] = name, pswrd
        self.base.sync()

    def removeUser(self, key):
        del self.base[key]
        self.base.sync()

    def keyInBase(self, key):
        return key in self.base.keys()

    def getUser(self, key):
        return self.base[key]

    def close(self):
        self.base.close()
