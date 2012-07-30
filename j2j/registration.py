from twilix.register import RegisterQuery
from twilix import fields

from dbase import UserBase

class RegisterHandler(RegisterQuery):

    username = fields.StringNode('username', required=False)
    password = fields.StringNode('password', required=False)
    base = UserBase('users')

    def getHandler(self):
        from_ = self.iq.from_.bare()
        if base.keyInBase(from_):

        reply = RegisterHandler(parent=self.makeResult())
        reply.instructions = 'Enter username and password!'
        reply.username = ''
        reply.password = ''
        return reply

    def setHandler(self):
        from_ = self.iq.from_.bare()
        if not base.keyInBase(from_):
            base.addUser(from_, self.username, self.password)
            reply = RegisterHandler(parent=self.makeResult())
            reply.registered = ''
            reply.username, reply.password = self.username, self.password
            return reply
        else:

        elif base.userInBase(self.username):
            raise errors.NotAcceptable('Username already exists')
        if self.aremove:
            raise errors.RegistrationRequired
        print self.username
        print self.password
        return self.makeResult()
