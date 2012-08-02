from twisted.internet import reactor
from twilix.register import RegisterQuery
from twilix import fields
from twilix import errors
from twilix.stanzas import Presence

class RegisterHandler(RegisterQuery):

    username = fields.StringNode('username', required=False)
    password = fields.StringNode('password', required=False)

    def getHandler(self):
        from_ = self.iq.from_
        reply = RegisterHandler(parent=self.makeResult())
        if self.host.dbase.keyInBase(str(from_.userhost())):
            reply.username, reply.password = self.host.dbase.getUser(
                                                        str(from_.userhost()))
            reply.registered = ''
            return reply
        reply.instructions = 'Enter username and password!'
        reply.username = ''
        reply.password = ''
        return reply

    def setHandler(self):
        from_ = self.iq.from_
        if not self.host.dbase.keyInBase(str(from_.userhost())):
            if self.aremove:
                raise errors.RegistrationRequiredException
            self.host.dbase.addUser(str(from_.userhost()),
                                    self.username, self.password)
            reply1 = RegisterHandler(parent=self.makeResult())
            reply1.username, reply1.password = self.username, self.password
            reply2 = Presence(from_=self.iq.to,
                              to=from_.bare(), type_='subscribe')
            return reply1, reply2
        else:
            if self.aremove:
                self.host.dbase.removeUser(str(from_.userhost()))
                return self.makeResult()
            user, passw = self.host.dbase.getUser(str(from_.userhost()))
            if self.username != user:
                for client in self.host.pool.pool.values():
                    client.xmlstream.sendFooter()
                    reactor.callLater(1, client.connector.disconnect)
            self.host.dbase.addUser(str(from_.userhost()),
                              self.username, self.password)
            return self.makeResult()
        return self.makeResult()
