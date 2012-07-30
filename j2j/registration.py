from twilix.register import RegisterQuery
from twilix import fields
from twilix import errors

from dbase import UserBase

class RegisterHandler(RegisterQuery):

    username = fields.StringNode('username', required=False)
    password = fields.StringNode('password', required=False)
    base = UserBase('users')

    def getHandler(self):
        from_ = self.iq.from_
        reply = RegisterHandler(parent=self.makeResult())
        if self.base.keyInBase(str(from_.userhost())):
            reply.username, reply.password = self.base.getUser(
                                                        str(from_.userhost()))
            reply.registered = ''
            return reply
        reply.instructions = 'Enter username and password!'
        reply.username = ''
        reply.password = ''
        return reply

    def setHandler(self):
        from_ = self.iq.from_
        if not self.base.keyInBase(str(from_.userhost())):
            if self.aremove:
                raise errors.RegistrationRequiredException
            self.base.addUser(str(from_.userhost()),
                              self.username, self.password)
            reply = RegisterHandler(parent=self.makeResult())
            reply.username, reply.password = self.username, self.password
            return reply
        else:
            if self.aremove:
                self.base.removeUser(str(from_.userhost()))
                return self.makeResult()
            self.base.addUser(str(from_.userhost()),
                              self.username, self.password)
            return self.makeResult()
        return self.makeResult()
