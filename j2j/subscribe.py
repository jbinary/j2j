from twisted.internet.defer import inlineCallbacks, returnValue
from twisted.words.protocols.jabber.sasl import SASLAuthError
from twisted.internet.error import DNSLookupError

from twilix.stanzas import Presence
from twilix.base.myelement import EmptyStanza
from twilix import errors

from j2jClient import j2jClient, ClientPool
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

    def __init__(self, *args, **kwargs):
        super(PresenceHandler, self).__init__(*args, **kwargs)
        self.pool = ClientPool()

    def clean_from_(self, value):
        key = str(value.userhost())
        try:
            username, password = self.host.dbase.getUser(key)
        except KeyError:
            raise errors.RegistrationRequiredException
        self.username, self.password = username, password
        return value

    @inlineCallbacks
    def availableHandler(self):
        if self.username in self.pool.pool.keys():
            returnValue(self.get_reply())
        client = j2jClient(self.username)
        try:
            yield client.connect(self.password)
            self.pool.addClient(self.username, client)
        except DNSLookupError:
            raise errors.NotAcceptableException
        except SASLAuthError:
            raise errors.NotAuthorizedException
        except DuplicateClientsException:
            pass
        except Exception:
            raise errors.InternalServerErrorException
        returnValue(self.get_reply())

    def unavailableHandler(self):
        try:
            self.pool.removeClient(self.username)
        except WrongClientException:
            pass
        reply = self.get_reply()
        reply.type_ = 'unavailable'
        return reply
