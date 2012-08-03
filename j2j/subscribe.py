from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.words.protocols.jabber.sasl import SASLAuthError
from twisted.internet.error import DNSLookupError

from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza
from twilix.jid import internJID
from twilix import errors

from j2jClient import j2jClient
from j2jClient import WrongClientException, DuplicateClientsException

class SubscrHandler(Presence):

    def probeHandler(self):
        reply = self.get_reply()
        reply.to = reply.to.bare()
        reply.type_ = 'probe'
        return reply

    def subscribeHandler(self):
        reply1 = self.get_reply()
        reply1.type_ = 'subscribed'
        return reply1, self.probeHandler()

    def subscribedHandler(self):
        return EmptyStanza()

    def unsubscribedHandler(self):
        reply = Presence(to=self.from_, from_=self.to, type_='unsubscribed')
        return reply

class PresenceHandler(Presence):

    def clean_from_(self, value):
        key = str(value.userhost())
        try:
            guestJID, guestPass = self.host.dbase.getUser(key)
        except KeyError:
            raise errors.RegistrationRequiredException
        self.guestJID, self.guestPass = guestJID, guestPass
        return value

    @inlineCallbacks
    def availableHandler(self):
        name = u'%s/%s' % (self.guestJID, self.from_.resource)
        jid = internJID(name)
        if jid in self.host.pool.pool.keys():
            returnValue(EmptyStanza())
        try:
            client = j2jClient(name)
            self.host.pool.addClient(self.from_, client)
            yield client.connect(self.guestPass)
        except DNSLookupError:
            self.host.pool.removeClient(self.from_)
            raise errors.NotAcceptableException
        except SASLAuthError:
            self.host.pool.removeClient(self.from_)
            raise errors.NotAuthorizedException
        except DuplicateClientsException:
            pass
        except Exception:
            self.host.pool.removeClient(self.from_)
            raise errors.InternalServerErrorException
        returnValue(self.get_reply())

        def unavailableHandler(self):
            for u in self.host.pool.pool.keys():
                if u.bare() == self.from_.bare():
                    self.host.pool.pool[u].disconnect()
                    self.host.pool.removeClient(u)
            return EmptyStanza()
