import sqlite3

class UserBase(object):
    """
    Class describes interaction with sqlite database.
    """
    def __init__(self, path):
        self.base = sqlite3.connect(path)
        c = self.base.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS users \
                        (id integer PRIMARY KEY, \
                         user_jid text UNIQUE NOT NULL,\
                         guest_jid text NOT NULL,\
                         guest_pswd text NOT NULL)')
        self.base.commit()
        c.close()

    def addUser(self, userJID, guestJID, guestPswd):
        c = self.base.cursor()
        t = (userJID, guestJID, guestPswd)
        c.execute('INSERT INTO users (user_jid, guest_jid, guest_pswd) \
                        VALUES (?,?,?)', t)
        self.base.commit()
        c.close()

    def updateUser(self, userJID, guestJID, guestPswd):
        c = self.base.cursor()
        t = (guestJID, guestPswd, userJID)
        c.execute('UPDATE users SET guest_jid = ?, guest_pswd = ? \
                        WHERE user_jid = ?', t)
        self.base.commit()
        c.close()

    def userInBase(self, userJID):
        c = self.base.cursor()
        c.execute('SELECT * FROM users WHERE user_jid = ?', (userJID, ))
        ret = c.fetchone()
        c.close()
        if ret is None:
            return False
        return True

    def removeUser(self, userJID):
        c = self.base.cursor()
        c.execute('DELETE FROM users WHERE user_jid = ?', (userJID, ))
        self.base.commit()
        c.close()

    def getGuestJID(self, userJID):
        c = self.base.cursor()
        c.execute('SELECT guest_jid, guest_pswd FROM users \
                        WHERE user_jid = ?', (userJID, ))
        t = c.fetchone()
        c.close()
        if t == ():
            raise KeyError("There's no such user (%s) in the base!" % userJID)
        return t
