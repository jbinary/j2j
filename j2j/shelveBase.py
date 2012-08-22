import shelve

class UserBase(object):
    """
    Class describes interaction with shelve data base
    """
    def __init__(self, path):
        self.base = shelve.open(path)

    def addUser(self, userJID, guestJID, guestPswd):
        self.base[userJID] = guestJID, guestPswd
        self.base.sync()

    def updateUser(self, userJID, guestJID, guestPswd):
        self.base[userJID] = guestJID, guestPswd
        self.base.sync()

    def removeUser(self, userJID):
        del self.base[userJID]
        self.base.sync()

    def userInBase(self, userJID):
        return userJID in self.base.keys()

    def getGuestJID(self, userJID):
        return self.base[userJID]

    def close(self):
        self.base.close()
