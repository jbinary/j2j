from twisted.internet import reactor

from twilix.register import RegisterQuery
from twilix import fields
from twilix import errors
from twilix.stanzas import Presence

class RegisterHandler(RegisterQuery):
    """
    Extends RegisterQuery class.
    Defines get/set handlers for register queries.
    
    Attributes:
        username -- string node 'username' represents guest jid
        
        password -- string node 'password' represents guest password
    """
    username = fields.StringNode('username', required=False)
    password = fields.StringNode('password', required=False)

    def getHandler(self):
        """
        Calls from dispatcher when there is get register query.
        
        Returns iq stanza with instructions or,
        if the user is already registered, with registered data.
        """
        from_ = self.iq.from_
        reply = RegisterHandler(parent=self.makeResult())
        if self.host.dbase.userInBase(str(from_.userhost())):
            reply.username, reply.password = self.host.dbase.getGuestJID(
                                                        str(from_.userhost()))
            reply.registered = ''
            return reply
        reply.instructions = 'Enter username and password!'
        reply.username = ''
        reply.password = ''
        return reply

    def setHandler(self):
        """
        Calls from dispatcher when there is set register query.
        
        Returns iq stanza with 'result' type.
        
        :raises:
            RegistrationRequiredException
        """
        from_ = self.iq.from_
        if not self.host.dbase.userInBase(str(from_.userhost())):
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
            user, passw = self.host.dbase.getGuestJID(str(from_.userhost()))
            if self.username != user:
                for u in self.host.pool.pool.keys():
                    if u.bare() == from_.bare():
                        self.host.pool.pool[u].disconnect()
                        self.host.pool.removeClient(u)
            self.host.dbase.updateUser(str(from_.userhost()),
                                             self.username, self.password)
            return self.makeResult()
        return self.makeResult()
